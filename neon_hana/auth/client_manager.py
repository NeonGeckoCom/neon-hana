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

from uuid import uuid4
from datetime import datetime
from threading import Lock
from time import time
from typing import Dict, Optional
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import DecodeError, ExpiredSignatureError
from ovos_utils import LOG
from ovos_utils.log import log_deprecation
from pydantic import ValidationError
from token_throttler import TokenThrottler, TokenBucket
from token_throttler.storage import RuntimeStorage

from neon_data_models.models.api.jwt import HanaToken
from neon_hana.mq_service_api import MQServiceManager
from neon_data_models.models.user import (User, NeonUserConfig,
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
        self._register_rph = config.get("registration_requests_per_hour", 4)
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
        log_deprecation("This property is deprecated with no replacement", "1.0.0")
        return self._authorized_clients

    def _create_tokens(self,
                       user_id: str,
                       client_id: str,
                       token_name: Optional[str] = None,
                       permissions: Optional[PermissionsConfig] = None,
                       **kwargs) -> (str, str, Dict[str, HanaToken]):
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
                                      token_name=token_name,
                                      creation_timestamp=creation_timestamp,
                                      last_refresh_timestamp=creation_timestamp,
                                      purpose="access")
        refresh_token_data = HanaToken(iss=self._jwt_issuer,
                                       sub=user_id,
                                       exp=refresh_expiration_timestamp,
                                       iat=creation_timestamp,
                                       jti=f"{token_id}.refresh",
                                       client_id=client_id,
                                       roles=permissions.to_roles(),
                                       token_name=token_name,
                                       creation_timestamp=creation_timestamp,
                                       last_refresh_timestamp=creation_timestamp,
                                       purpose="refresh")
        access_token = jwt.encode(access_token_data.model_dump(),
                                  self._access_secret, self._jwt_algo)
        refresh_token = jwt.encode(refresh_token_data.model_dump(),
                                   self._refresh_secret, self._jwt_algo)

        return access_token, refresh_token, {"access": access_token_data,
                                             "refresh": refresh_token_data}

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

    def _consume_rate_limit_token(self, ratelimit_id: str):
        if not self.rate_limiter.consume(ratelimit_id):
            bucket = list(self.rate_limiter.get_all_buckets(ratelimit_id).
                          values())[0]
            replenish_time = bucket.last_replenished + bucket.replenish_time
            wait_time = round(replenish_time - time())
            ip_addr, request_cls = ratelimit_id.split('-', 1)
            raise HTTPException(status_code=429,
                                detail=f"Too many {request_cls} requests from: "
                                       f"{ip_addr}. Wait {wait_time}s.")

    def check_registration_request(self, username: str, password: str,
                                   user_config: NeonUserConfig,
                                   origin_ip: str = "127.0.0.1") -> User:
        """
        Handle a request to register a new user.
        """

        ratelimit_id = f"{origin_ip}-register"
        if not self.rate_limiter.get_all_buckets(ratelimit_id):
            self.rate_limiter.add_bucket(ratelimit_id,
                                         TokenBucket(replenish_time=3600,
                                                     max_tokens=self._register_rph))
        self._consume_rate_limit_token(ratelimit_id)

        new_user = User(username=username, password_hash=password,
                        neon=user_config, permissions=_DEFAULT_USER_PERMISSIONS)
        if self._mq_connector:
            return self._mq_connector.create_user(new_user)
        else:
            LOG.debug("No User Database connected. Return valid registration.")
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

        ratelimit_id = f"{origin_ip}-auth"
        if not self.rate_limiter.get_all_buckets(ratelimit_id):
            self.rate_limiter.add_bucket(ratelimit_id,
                                         TokenBucket(replenish_time=60,
                                                     max_tokens=self._auth_rpm))
        self._consume_rate_limit_token(ratelimit_id)

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
            user = self._mq_connector.read_user(username, password)

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
                                               expiration=config['access'].exp)
        self.authorized_clients[client_id] = auth_response
        self._add_token_to_userdb(user, config['refresh'])
        return auth_response

    def check_refresh_request(self, access_token: Optional[str],
                              refresh_token: str,
                              client_id: str) -> AuthenticationResponse:
        # Read and validate refresh token
        try:
            refresh_data = HanaToken(**jwt.decode(refresh_token,
                                                  self._refresh_secret,
                                                  self._jwt_algo))
            token_data = HanaToken(**jwt.decode(access_token,
                                                self._access_secret,
                                                self._jwt_algo,
                                                options={"verify_signature": False}))
            if refresh_data.purpose != "refresh":
                raise HTTPException(status_code=400,
                                    detail="Supplied refresh token not valid")
            # if token_data.purpose != "access":
            #     raise HTTPException(status_code=400,
            #                         detail="Supplied refresh token not valid")
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

        if refresh_data.client_id != client_id:
            raise HTTPException(status_code=403,
                                detail="Access token does not match client_id")

        encode_data = {"user_id": refresh_data.sub,
                       "client_id": client_id,
                       "token_name": refresh_data.token_name,
                       "permissions": PermissionsConfig.from_roles(refresh_data.roles)
                       }
        access, refresh, tokens = self._create_tokens(**encode_data)
        username = refresh_data.sub
        if self._mq_connector:
            user = self._mq_connector.read_user(username=refresh_data.sub,
                                                access_token=token_data)
            if not user.password_hash:
                # This should not be possible, but don't let an error in the
                # users service allow for injecting a new valid token to the db
                raise HTTPException(status_code=500, detail="Error Fetching User")
            self._add_token_to_userdb(user, tokens['refresh'])

        auth_response = AuthenticationResponse(username=username,
                                               client_id=client_id,
                                               access_token=access,
                                               refresh_token=refresh,
                                               expiration=tokens['refresh'].exp)
        self._authorized_clients[client_id] = auth_response
        return auth_response

    def _add_token_to_userdb(self, user: User, new_token: HanaToken):
        if new_token.purpose != "refresh":
            raise ValueError(f"Expected a refresh token, got: "
                             f"{new_token.purpose}")
        if self._mq_connector is None:
            LOG.debug("No MQ Connection to a user database")
            return
        for idx, token in enumerate(user.tokens):
            # If the token is already defined, maintain the original
            # creation timestamp
            if token.jti == new_token.jti:
                new_token.creation_timestamp = token.creation_timestamp
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

    def get_token_data(self, token: str) -> HanaToken:
        """
        Extract the user_id from a JWT string
        @param token: JWT to parse
        @retrun: user_id associated with token
        """
        return HanaToken(**jwt.decode(token, self._access_secret,
                                      self._jwt_algo))

    def validate_auth(self, token: str, origin_ip: str) -> bool:
        ratelimit_id = f"{origin_ip}-total"
        if not self.rate_limiter.get_all_buckets(ratelimit_id):
            self.rate_limiter.add_bucket(ratelimit_id,
                                         TokenBucket(replenish_time=60,
                                                     max_tokens=self._rpm))
        if self._rpm > 0:
            self._consume_rate_limit_token(ratelimit_id)

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
        except ValidationError:
            LOG.error(f"Invalid token data received from {origin_ip}.")
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
