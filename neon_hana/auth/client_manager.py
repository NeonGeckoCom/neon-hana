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
from threading import Lock

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
from neon_hana.mq_service_api import MQServiceManager
from neon_data_models.models.user import (User, TokenConfig, NeonUserConfig,
                                          PermissionsConfig)
from neon_data_models.enum import AccessRoles

_DEFAULT_USER_PERMISSIONS = PermissionsConfig(klat=AccessRoles.USER,
                                              core=AccessRoles.USER,
                                              diana=AccessRoles.USER,
                                              node=AccessRoles.USER,
                                              hub=AccessRoles.USER,
                                              llm=AccessRoles.USER)


class ClientManager:
    def __init__(self, config: dict,
                 mq_connector: Optional[MQServiceManager] = None):
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
        self._node_username = config.get("node_username")
        self._node_password = config.get("node_password")
        self._max_streaming_clients = config.get("max_streaming_clients")
        self._jwt_algo = "HS256"
        self._connected_streams = 0
        self._stream_check_lock = Lock()
        self._mq_connector = mq_connector

    def _create_tokens(self, encode_data: dict) -> TokenConfig:
        # Permissions were not included in old tokens, allow refreshing with
        # default permissions
        encode_data.setdefault("permissions", ClientPermissions().as_dict())

        token_expiration = encode_data['expire']
        token = jwt.encode(encode_data, self._access_secret, self._jwt_algo)
        encode_data['expire'] = round(time()) + self._refresh_token_lifetime
        encode_data['access_token'] = token
        refresh = jwt.encode(encode_data, self._refresh_secret, self._jwt_algo)
        return TokenConfig(**{"username": encode_data['username'],
                              "client_id": encode_data['client_id'],
                              "permissions": encode_data['permissions'],
                              "access_token": token,
                              "refresh_token": refresh,
                              "expiration": token_expiration,
                              "refresh_expiration": encode_data['expire'],
                              "token_name": encode_data['name'],
                              "creation_timestamp": encode_data['create'],
                              "last_refresh_timestamp": encode_data['last_refresh_timestamp']
                              })

    def get_permissions(self, client_id: str) -> ClientPermissions:
        """
        Get ClientPermissions model for the given client_id
        @param client_id: Client ID to get permissions for
        @return: ClientPermissions object for the specified client
        """
        if self._disable_auth:
            LOG.debug("Auth disabled, allow full client permissions")
            return ClientPermissions(assist=True, backend=True, node=True)
        if client_id not in self.authorized_clients:
            LOG.warning(f"{client_id} not known to this server")
            return ClientPermissions(assist=False, backend=False, node=False)
        client = self.authorized_clients[client_id]
        return ClientPermissions(**client.get('permissions', dict()))

    def check_connect_stream(self) -> bool:
        """
        Check if a new stream is allowed
        """
        with self._stream_check_lock:
            if not isinstance(self._max_streaming_clients, int) or \
                    self._max_streaming_clients is False or \
                    self._max_streaming_clients < 0:
                self._connected_streams += 1
                return True
            if self._connected_streams >= self._max_streaming_clients:
                LOG.warning(f"No more streams allowed ({self._connected_streams})")
                return False
            self._connected_streams += 1
            return True

    def disconnect_stream(self):
        with self._stream_check_lock:
            self._connected_streams -= 1

    def check_registration_request(self, username: str, password: str,
                                   user_config: NeonUserConfig) -> User:
        """
        Handle a request to register a new user.
        """
        new_user = User(username=username, password_hash=password,
                        neon=user_config, permissions=_DEFAULT_USER_PERMISSIONS)
        if self._mq_connector:
            return self._mq_connector.create_user(new_user)
        else:
            print("No User Database connected. Return valid registration.")
            return new_user

    def check_auth_request(self, client_id: str, username: str,
                           password: Optional[str] = None,
                           token_name: Optional[str] = None,
                           origin_ip: str = "127.0.0.1") -> dict:
        """
        Authenticate and Authorize a new client connection with the specified
        username, password, and origin IP address.
        @param client_id: Client ID of the connection to auth
        @param username: Supplied username to authenticate
        @param password: Supplied password to authenticate
        @param token_name: Token name to add to user database
        @param origin_ip: Origin IP address of request
        @return: response tokens, permissions, and other metadata
        """
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

        if self._mq_connector is None:
            user = User(username=username, password_hash=password)
        elif all((self._node_username, username == self._node_username,
                  password == self._node_password)):
            user = User(username=username, password_hash=password)
            user.permissions.node = AccessRoles.USER
        else:
            user = self._mq_connector.get_user_profile(username, password)
            username = user.username

        # Boolean permissions allow access for any role, including `NODE`.
        # Specific endpoints may enforce more granular controls/limits based on
        # specific user.permissions values.
        permissions = ClientPermissions(
            node=user.permissions.node != AccessRoles.NONE,
            assist=user.permissions.core != AccessRoles.NONE,
            backend=user.permissions.diana != AccessRoles.NONE)
        create_time = round(time())
        expiration = create_time + self._access_token_lifetime
        encode_data = {"client_id": client_id,
                       "sub": username,  # Added for Klat token compat.
                       "name": token_name,
                       "username": username,
                       "permissions": permissions.as_dict(),
                       "create": create_time,
                       "expire": expiration,
                       "last_refresh_timestamp": create_time}
        auth = self._create_tokens(encode_data)
        self._add_token_to_userdb(user, auth)
        self.authorized_clients[client_id] = auth.model_dump()
        return auth.model_dump()

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

        if self._mq_connector:
            user = self._mq_connector.get_user_profile(username=token_data['username'],
                                                       access_token=refresh_token)
            if not user.password_hash:
                # This should not be possible, but don't let an error in the
                # users service allow for injecting a new valid token to the db
                raise HTTPException(status_code=500, detail="Error Fetching User")
            refresh_time = round(time())
            encode_data['last_refresh_timestamp'] = refresh_time
            encode_data["expire"] = refresh_time + self._access_token_lifetime
            new_auth = self._create_tokens(encode_data)
            self._add_token_to_userdb(user, new_auth)
        else:
            new_auth = self._create_tokens(encode_data)
        return new_auth.model_dump()

    def _add_token_to_userdb(self, user: User, token_data: TokenConfig):
        if self._mq_connector is None:
            print("No MQ Connection to a user database")
            return
        # Enforce unique `creation_timestamp` values to avoid duplicate entries
        for idx, token in enumerate(user.tokens):
            if token.creation_timestamp == token_data.creation_timestamp:
                user.tokens.remove(token)
        user.tokens.append(token_data)
        self._mq_connector.update_user(user)

    def get_client_id(self, token: str) -> str:
        """
        Extract the client_id from a JWT token
        @param token: JWT token to parse
        @return: client_id associated with token
        """
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
            host = request.client.host if request.client else "127.0.0.1"
            if not self.client_manager.validate_auth(credentials.credentials,
                                                     host):
                raise HTTPException(status_code=403,
                                    detail="Invalid or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403,
                                detail="Invalid or missing auth credentials.")
