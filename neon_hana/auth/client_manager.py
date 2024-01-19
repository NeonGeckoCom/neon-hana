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
from token_throttler import TokenThrottler, TokenBucket
from token_throttler.storage import RuntimeStorage


class ClientManager:
    def __init__(self, config: dict):
        self.rate_limiter = TokenThrottler(cost=1, storage=RuntimeStorage())

        self.authorized_clients: Dict[str, dict] = dict()
        self._access_token_lifetime = config.get("access_token_ttl", 3600 * 24)
        self._refresh_token_lifetime = config.get("refresh_token_ttl",
                                                  3600 * 24 * 7)
        self._access_secret = config.get("access_token_secret") or "a800445648142061fc238d1f84e96200da87f4f9f784108ac90db8b4391b117b"
        self._refresh_secret = config.get("refresh_token_secret") or "a800445648142061fc238d1f84e96200da87f4f9f784108ac90db8b4391b117b"
        self._rpm = config.get("requests_per_minute", 60)
        self._disable_auth = config.get("disable_auth")
        self._jwt_algo = "HS256"

    def _create_tokens(self, encode_data: dict) -> dict:
        token = jwt.encode(encode_data, self._access_secret, self._jwt_algo)
        encode_data['expire'] = time() + self._refresh_token_lifetime
        encode_data['access_token'] = token
        refresh = jwt.encode(encode_data, self._refresh_secret, self._jwt_algo)
        # TODO: Store refresh token on server to allow invalidating clients
        return {"username": encode_data['username'],
                "client_id": encode_data['client_id'],
                "access_token": token,
                "refresh_token": refresh}

    def check_auth_request(self, client_id: str, username: str,
                           password: Optional[str] = None):
        if client_id in self.authorized_clients:
            return self.authorized_clients[client_id]
        if username != "guest":
            # TODO: Validate password here
            pass
        expiration = time() + self._access_token_lifetime
        encode_data = {"client_id": client_id,
                       "username": username,
                       "password": password,
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
        try:
            token_data = jwt.decode(access_token, self._access_secret,
                                    self._jwt_algo)
        except DecodeError:
            raise HTTPException(status_code=400,
                                detail="Invalid access token supplied")
        if token_data['client_id'] != client_id:
            raise HTTPException(status_code=403,
                                detail="Access token does not match client_id")
        encode_data = {k: token_data[k] for k in
                       ("client_id", "username", "password")}
        encode_data["expire"] = time() + self._access_token_lifetime
        new_auth = self._create_tokens(encode_data)
        return new_auth

    def validate_auth(self, token: str, origin_ip: str) -> bool:
        if not self.rate_limiter.get_all_buckets(origin_ip):
            self.rate_limiter.add_bucket(origin_ip,
                                         TokenBucket(replenish_time=60,
                                                     max_tokens=self._rpm))
        if not self.rate_limiter.consume(origin_ip) and self._rpm > 0:
            raise HTTPException(status_code=429,
                                detail=f"Requests limited to {self._rpm}/min"
                                       f"per client connection")

        if self._disable_auth:
            return True
        try:
            auth = jwt.decode(token, self._access_secret, self._jwt_algo)
            if auth['expire'] < time():
                self.authorized_clients.pop(auth['client_id'], None)
                return False
            # Keep track of authorized client connections
            self.authorized_clients[auth['client_id']] = auth
            # TODO: Consider consuming an extra request for guest sessions
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