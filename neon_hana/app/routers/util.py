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

import re

from fastapi import APIRouter, Request
from starlette.responses import PlainTextResponse

from neon_hana.app.dependencies import client_manager

util_route = APIRouter(prefix="/util", tags=["utilities"])


def _is_ipv4(address: str) -> bool:
    ipv4_regex = re.compile(
        r'^(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01'
        r']?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|'
        r'2[0-4][0-9]|[01]?[0-9][0-9]?)$')
    return ipv4_regex.match(address)


@util_route.get("/client_ip", response_class=PlainTextResponse)
async def api_client_ip(request: Request) -> str:
    ip_addr = request.client.host if request.client else "127.0.0.1"

    if not _is_ipv4(ip_addr):
        # Reported host is a hostname, not an IP address. Return a generic
        # loopback value
        ip_addr = "127.0.0.1"
    client_manager.validate_auth("", ip_addr)
    return ip_addr


@util_route.get("/headers")
async def api_headers(request: Request):
    ip_addr = request.client.host if request.client else "127.0.0.1"
    client_manager.validate_auth("", ip_addr)
    return request.headers
