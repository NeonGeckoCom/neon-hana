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

from fastapi import APIRouter, Depends
from neon_hana.schema.llm_requests import *
from neon_hana.app.dependencies import jwt_bearer, mq_connector


llm_route = APIRouter(prefix="/llm", tags=["backend"],
                      dependencies=[Depends(jwt_bearer)])


@llm_route.post("/chatgpt")
async def llm_ask_chatgpt(query: LLMRequest) -> LLMResponse:
    return mq_connector.query_llm("chat_gpt", **dict(query))


@llm_route.post("/fastchat")
async def llm_ask_fastchat(query: LLMRequest) -> LLMResponse:
    return mq_connector.query_llm("fastchat", **dict(query))


@llm_route.post("/gemini")
async def llm_ask_gemini(query: LLMRequest) -> LLMResponse:
    return mq_connector.query_llm("gemini", **dict(query))


@llm_route.post("/claude")
async def llm_ask_claude(query: LLMRequest) -> LLMResponse:
    return mq_connector.query_llm("claude", **dict(query))


@llm_route.post("/palm")
async def llm_ask_palm(query: LLMRequest) -> LLMResponse:
    return mq_connector.query_llm("palm2", **dict(query))
