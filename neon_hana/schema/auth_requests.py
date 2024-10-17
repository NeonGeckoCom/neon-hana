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

from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class AuthenticationRequest(BaseModel):
    username: str = "guest"
    password: Optional[str] = None
    client_id: str = Field(default_factory=lambda: str(uuid4()))

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "username": "guest",
                "password": "password"
            }]}}


class AuthenticationResponse(BaseModel):
    username: str
    client_id: str
    access_token: str
    refresh_token: str
    expiration: float

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "username": "guest",
                "client_id": "be84ae66-f61c-4aac-a9af-b0da364b82b6",
                "access_token": "<redacted>",
                "refresh_token": "<redacted>",
                "expiration": 1706045776.4168212
            }]}}


class RefreshRequest(BaseModel):
    access_token: str
    refresh_token: str
    client_id: str


class PermissionsRequest(BaseModel):
    access_token: str
    client_id: str
