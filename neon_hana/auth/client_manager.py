# NEON AI (TM) SOFTWARE, Software Development Kit & Application Development System
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2021 Neongecko.com Inc.
# BSD-3
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE,  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import jwt

from time import time
from typing import Dict, Optional
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import DecodeError
from ovos_utils import LOG
from token_throttler import TokenThrottler, TokenBucket
from token_throttler.storage import RuntimeStorage

from neon_hana.auth.permissions import ClientPermissions


class ClientManager:
    def __init__(self, config: dict):
        self.rate_limiter = TokenThrottler(cost=1, storage=RuntimeStorage())

        self.authorized_clients: Dict[str, dict] = dict()
        self._access_token_lifetime = config.get("access_token_ttl", 3600 * 24)
        self._refresh_token_lifetime = config.get("refresh_token_ttl",
                                                  3600 * 24 * 7)
        self._access_secret = config.get("access_token_secret")
        self._refresh_secret = config.get("refresh_token_secret")
        self._rpm = config.get("requests_per_minute", 60)
        self._auth_rpm = config.get("auth_requests_per_minute", 6)
        self._disable_auth = config.get("disable_auth")
        self._jwt_algo = "HS256"

    def _create_tokens(self, encode_data: dict) -> dict:
        token_expiration = encode_data['expire']
        token = jwt.encode(encode_data, self._access_secret, self._jwt_algo)
        encode_data['expire'] = time() + self._refresh_token_lifetime
        encode_data['access_token'] = token
        refresh = jwt.encode(encode_data, self._refresh_secret, self._jwt_algo)
        # TODO: Store refresh token on server to allow invalidating clients
        return {"username": encode_data['username'],
                "client_id": encode_data['client_id'],
                "permissions": encode_data['permissions'],
                "access_token": token,
                "refresh_token": refresh,
                "expiration": token_expiration}

    def get_permissions(self, client_id: str) -> ClientPermissions:
        """
        Get ClientPermissions model for the given client_id
        @param client_id: Client ID to get permissions for
        @return: ClientPermissions object for the specified client
        """
        if self._disable_auth:
            return ClientPermissions(assist=True, backend=True, node=True)
        if client_id not in self.authorized_clients:
            LOG.warning(f"{client_id} not known to this server")
            return ClientPermissions(assist=False, backend=False, node=False)
        client = self.authorized_clients[client_id]
        return ClientPermissions(**client.get('permissions', dict()))

    def check_auth_request(self, client_id: str, username: str,
                           password: Optional[str] = None,
                           origin_ip: str = "127.0.0.1"):
        if client_id in self.authorized_clients:
            print(f"Using cached client: {self.authorized_clients[client_id]}")
            return self.authorized_clients[client_id]

        ratelimit_id = f"auth{origin_ip}"
        if not self.rate_limiter.get_all_buckets(ratelimit_id):
            self.rate_limiter.add_bucket(ratelimit_id,
                                         TokenBucket(replenish_time=60,
                                                     max_tokens=self._auth_rpm))
        if not self.rate_limiter.consume(ratelimit_id):
            bucket = list(self.rate_limiter.get_all_buckets(ratelimit_id).
                          values())[0]
            replenish_time = bucket.last_replenished + bucket.replenish_time
            wait_time = round(replenish_time - time())
            raise HTTPException(status_code=429,
                                detail=f"Too many auth requests from: "
                                       f"{origin_ip}. Wait {wait_time}s.")

        node_access = False
        if username != "guest":
            # TODO: Validate password here
            pass
        # TODO: Configurable username/password here
        if username == "node_user" and password == "node_password":
            node_access = True
        permissions = ClientPermissions(node=node_access)
        expiration = time() + self._access_token_lifetime
        encode_data = {"client_id": client_id,
                       "username": username,
                       "password": password,
                       "permissions": permissions.as_dict(),
                       "expire": expiration}
        auth = self._create_tokens(encode_data)
        self.authorized_clients[client_id] = auth
        return auth

    def check_refresh_request(self, access_token: str, refresh_token: str,
                              client_id: str):
        # Read and validate refresh token
        try:
            refresh_data = jwt.decode(refresh_token, self._refresh_secret,
                                      self._jwt_algo)
        except DecodeError:
            raise HTTPException(status_code=400,
                                detail="Invalid refresh token supplied")
        if refresh_data['access_token'] != access_token:
            raise HTTPException(status_code=403,
                                detail="Refresh and access token mismatch")
        if time() > refresh_data['expire']:
            raise HTTPException(status_code=401,
                                detail="Refresh token is expired")
        # Read access token and re-generate a new pair of tokens
        # This is already known to be a valid token based on the refresh token
        token_data = jwt.decode(access_token, self._access_secret,
                                self._jwt_algo)

        if token_data['client_id'] != client_id:
            raise HTTPException(status_code=403,
                                detail="Access token does not match client_id")
        encode_data = {k: token_data[k] for k in
                       ("client_id", "username", "password")}
        encode_data["expire"] = time() + self._access_token_lifetime
        new_auth = self._create_tokens(encode_data)
        return new_auth

    def get_client_id(self, token: str):
        auth = jwt.decode(token, self._access_secret, self._jwt_algo)
        return auth['client_id']

    def validate_auth(self, token: str, origin_ip: str) -> bool:
        if not self.rate_limiter.get_all_buckets(origin_ip):
            self.rate_limiter.add_bucket(origin_ip,
                                         TokenBucket(replenish_time=60,
                                                     max_tokens=self._rpm))
        if not self.rate_limiter.consume(origin_ip) and self._rpm > 0:
            raise HTTPException(status_code=429,
                                detail=f"Requests limited to {self._rpm}/min "
                                       f"per client connection")

        if self._disable_auth:
            return True
        try:
            auth = jwt.decode(token, self._access_secret, self._jwt_algo)
            if auth['expire'] < time():
                self.authorized_clients.pop(auth['client_id'], None)
                return False
            self.authorized_clients[auth['client_id']] = auth
            return True
        except DecodeError:
            # Invalid token supplied
            pass
        return False


class UserTokenAuth(HTTPBearer):
    def __init__(self, client_manager: ClientManager):
        HTTPBearer.__init__(self)
        self.client_manager = client_manager

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = \
            await HTTPBearer.__call__(self, request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403,
                                    detail="Invalid authentication scheme.")
            if not self.client_manager.validate_auth(credentials.credentials,
                                                     request.client.host):
                raise HTTPException(status_code=403,
                                    detail="Invalid or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403,
                                detail="Invalid or missing auth credentials.")
