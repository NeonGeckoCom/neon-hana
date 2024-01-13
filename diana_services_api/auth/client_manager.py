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


class ClientManager:
    def __init__(self):
        self.authorized_clients: Dict[str, dict] = dict()
        # TODO: secrets and expirations from config
        self._access_token_lifetime = 3600 * 24  # 1 day
        self._refresh_token_lifetime = 3600 * 24 * 7  # 1 week
        self._access_secret = 'a800445648142061fc238d1f84e96200da87f4f9f784108ac90db8b4391b117b'
        self._refresh_secret = '833d369ac73d883123743a44b4a7fe21203cffc956f4c8a99be6e71aafa8e1aa'
        self._jwt_algo = "HS256"

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
        token = jwt.encode(encode_data, self._access_secret, self._jwt_algo)
        encode_data['expire'] = time() + self._refresh_token_lifetime
        refresh = jwt.encode(encode_data, self._refresh_secret, self._jwt_algo)
        # TODO: Store refresh token on server to validate refresh requests
        auth = {"username": username,
                "client_id": client_id,
                "access_token": token,
                "refresh_token": refresh}
        self.authorized_clients[client_id] = auth
        return auth

    def validate_auth(self, token: str) -> bool:
        try:
            auth = jwt.decode(token, self._access_secret, self._jwt_algo)
            if auth['expire'] < time():
                self.authorized_clients.pop(auth['client_id'], None)
                return False
            # Keep track of authorized client connections
            self.authorized_clients[auth['client_id']] = auth
            return True
        except DecodeError:
            # Invalid token supplied
            pass
        return False


class JWTBearer(HTTPBearer):
    def __init__(self, client_manager: ClientManager):
        HTTPBearer.__init__(self)
        self.client_manager = client_manager

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = \
            await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403,
                                    detail="Invalid authentication scheme.")
            if not self.client_manager.validate_auth(credentials.credentials):
                raise HTTPException(status_code=403,
                                    detail="Invalid or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403,
                                detail="Invalid or missing auth credentials.")
