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
from uuid import uuid4

import jwt

from datetime import datetime
from threading import Lock
from time import time
from typing import Dict, Optional
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import DecodeError, ExpiredSignatureError
from ovos_utils import LOG
from token_throttler import TokenThrottler, TokenBucket
from token_throttler.storage import RuntimeStorage

from neon_data_models.models.api.jwt import HanaToken
from neon_hana.mq_service_api import MQServiceManager
from neon_data_models.models.user import (User, TokenConfig, NeonUserConfig,
                                          PermissionsConfig)
from neon_data_models.enum import AccessRoles
from neon_hana.schema.auth_requests import AuthenticationResponse

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

        # Keep a dict of `client_id` to auth tokens that have authenticated to
        # this instance
        self._authorized_clients: Dict[str, AuthenticationResponse] = dict()
        self._access_token_lifetime = config.get("access_token_ttl", 3600 * 24)
        self._refresh_token_lifetime = config.get("refresh_token_ttl",
                                                  3600 * 24 * 90)
        self._jwt_issuer = config.get("jwt_issuer", "neon.ai")
        self._access_secret = config.get("access_token_secret")
        self._refresh_secret = config.get("refresh_token_secret")
        self._rpm = config.get("requests_per_minute", 60)
        self._auth_rpm = config.get("auth_requests_per_minute", 6)
        self._disable_auth = config.get("disable_auth")
        self._max_streaming_clients = config.get("max_streaming_clients")
        self._jwt_algo = "HS256"
        self._connected_streams = 0
        self._stream_check_lock = Lock()
        # If authentication is explicitly disabled, don't try to query the
        # users service
        self._mq_connector = None if self._disable_auth else mq_connector

    @property
    def authorized_clients(self) -> Dict[str, AuthenticationResponse]:
        """
        Dict of `client_id` to `AuthenticationResponse` objects for clients
        known by this instance. NOTE: Refresh tokens are not reliably stored
        here and should never be retrievable after generation for security.
        """
        # TODO: Is `authorized_clients` useful to track?
        return self._authorized_clients

    def _create_tokens(self,
                       user_id: str,
                       client_id: str,
                       token_name: Optional[str] = None,
                       permissions: Optional[PermissionsConfig] = None,
                       **kwargs) -> (str, str, TokenConfig):
        token_id = str(uuid4())
        # Subtract a second from creation so the token may be used immediately
        # upon return
        creation_timestamp = round(time()) - 1
        expiration_timestamp = creation_timestamp + self._access_token_lifetime
        refresh_expiration_timestamp = creation_timestamp + self._refresh_token_lifetime
        permissions = permissions or PermissionsConfig(core=AccessRoles.GUEST,
                                                       diana=AccessRoles.GUEST,
                                                       node=AccessRoles.GUEST,
                                                       llm=AccessRoles.GUEST)
        token_name = token_name or kwargs.get("name") or \
                     datetime.fromtimestamp(creation_timestamp).isoformat()
        access_token_data = HanaToken(iss=self._jwt_issuer,
                                      sub=user_id,
                                      exp=expiration_timestamp,
                                      iat=creation_timestamp,
                                      jti=token_id,
                                      client_id=client_id,
                                      roles=permissions.to_roles(),
                                      purpose="access")
        refresh_token_data = HanaToken(iss=self._jwt_issuer,
                                       sub=user_id,
                                       exp=refresh_expiration_timestamp,
                                       iat=creation_timestamp,
                                       jti=f"{token_id}.refresh",
                                       client_id=client_id,
                                       roles=permissions.to_roles(),
                                       purpose="refresh")
        access_token = jwt.encode(access_token_data.model_dump(),
                                  self._access_secret, self._jwt_algo)
        refresh_token = jwt.encode(refresh_token_data.model_dump(),
                                   self._refresh_secret, self._jwt_algo)
        token_config = TokenConfig(token_name=token_name,
                                   token_id=token_id,
                                   user_id=user_id,
                                   client_id=client_id,
                                   permissions=permissions,
                                   refresh_expiration_timestamp=refresh_expiration_timestamp,
                                   creation_timestamp=creation_timestamp,
                                   last_refresh_timestamp=creation_timestamp)
        return access_token, refresh_token, token_config

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
                           origin_ip: str = "127.0.0.1") -> AuthenticationResponse:
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
        # Caching does not work here because there is no guarantee that this
        # instance knows the client's refresh token. One client may also want
        # to generate multiple tokens.
        # if client_id in self.authorized_clients:
        #     print(f"Using cached client: {self.authorized_clients[client_id]}")
        #     return self.authorized_clients[client_id]

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
            # Auth is disabled; every auth request gets a successful response
            user = User(username=username, password_hash=password,
                        permissions=_DEFAULT_USER_PERMISSIONS)
        # elif all((self._node_username, username == self._node_username,
        #           password == self._node_password)):
        #     # User matches configured node username/password
        #     user = User(username=username, password_hash=password,
        #                 permissions=_DEFAULT_USER_PERMISSIONS)
        #     user.permissions.node = AccessRoles.USER
        else:
            user = self._mq_connector.get_user_profile(username, password)

        create_time = round(time())
        encode_data = {"client_id": client_id,
                       "user_id": user.user_id,
                       "permissions": user.permissions,
                       "token_name": token_name,
                       "last_refresh_timestamp": create_time}
        access, refresh, config = self._create_tokens(**encode_data)

        auth_response = AuthenticationResponse(username=user.username,
                                               client_id=client_id,
                                               access_token=access,
                                               refresh_token=refresh,
                                               expiration=config.refresh_expiration_timestamp)
        self.authorized_clients[client_id] = auth_response
        self._add_token_to_userdb(user, config)
        return auth_response

    def check_refresh_request(self, access_token: str, refresh_token: str,
                              client_id: str) -> AuthenticationResponse:
        # Read and validate refresh token
        try:
            refresh_data = HanaToken(**jwt.decode(refresh_token,
                                                  self._refresh_secret,
                                                  self._jwt_algo))
            token_data = HanaToken(**jwt.decode(access_token,
                                                self._access_secret,
                                                self._jwt_algo,
                                                leeway=self._refresh_token_lifetime))
        except DecodeError:
            raise HTTPException(status_code=400,
                                detail="Invalid token supplied")
        except ExpiredSignatureError:
            raise HTTPException(status_code=401,
                                detail="Refresh token is expired")
        if refresh_data.jti != token_data.jti + ".refresh":
            raise HTTPException(status_code=403,
                                detail="Refresh and access token mismatch")
        if time() > refresh_data.exp:
            raise HTTPException(status_code=401,
                                detail="Refresh token is expired")

        if token_data.client_id != client_id:
            raise HTTPException(status_code=403,
                                detail="Access token does not match client_id")

        # `token_name` is not known here, but it will be read from the database
        # when the new token replaces the old one
        encode_data = {"user_id": token_data.sub,
                       "client_id": client_id,
                       "permissions": PermissionsConfig.from_roles(token_data.roles)
                       }
        if self._mq_connector:
            user = self._mq_connector.get_user_profile(username=token_data.sub,
                                                       access_token=refresh_token)
            if not user.password_hash:
                # This should not be possible, but don't let an error in the
                # users service allow for injecting a new valid token to the db
                raise HTTPException(status_code=500, detail="Error Fetching User")
            access, refresh, config = self._create_tokens(**encode_data)
            username = user.username
            self._add_token_to_userdb(user, config)
        else:
            username = token_data.sub
            access, refresh, config = self._create_tokens(**encode_data)

        auth_response = AuthenticationResponse(username=username,
                                      client_id=client_id,
                                      access_token=access,
                                      refresh_token=refresh,
                                      expiration=config.refresh_expiration_timestamp)
        self._authorized_clients[client_id] = auth_response
        return auth_response

    def _add_token_to_userdb(self, user: User, new_token: TokenConfig):
        if self._mq_connector is None:
            print("No MQ Connection to a user database")
            return
        for idx, token in enumerate(user.tokens):
            if token.token_id == new_token.token_id:
                # Tokens don't contain `token_name`, so use the same one as is
                # being replaced
                new_token.token_name = token.token_name
                user.tokens.remove(token)
        user.tokens.append(new_token)
        self._mq_connector.update_user(user)

    def get_client_id(self, token: str) -> str:
        """
        Extract the client_id from a JWT string
        @param token: JWT to parse
        @return: client_id associated with token
        """
        auth = HanaToken(**jwt.decode(token, self._access_secret,
                                      self._jwt_algo))
        return auth.client_id

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
            auth = HanaToken(**jwt.decode(token, self._access_secret,
                                          self._jwt_algo))
            if auth.exp < time():
                self.authorized_clients.pop(auth.client_id, None)
                return False
            self.authorized_clients[auth.client_id] = AuthenticationResponse(
                username=auth.sub, client_id=auth.client_id, access_token=token,
                refresh_token="", expiration=auth.exp)
            return True
        except DecodeError:
            # Invalid token supplied
            pass
        except ExpiredSignatureError:
            # Expired token
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
