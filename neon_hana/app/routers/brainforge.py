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
from neon_hana.app.dependencies import jwt_bearer, mq_connector

from neon_data_models.models.api.http.brainforge import LLMGetModelsHttpResponse, LLMGetPersonasHttpRequest, \
    LLMGetPersonasHttpResponse, LLMGetInferenceHttpRequest
from neon_data_models.models.api.llm import LLMResponse
from neon_data_models.enum import AccessRoles


bf_route = APIRouter(prefix="/brainforge", tags=["llm"],
                     dependencies=[Depends(jwt_bearer)])

def _validate_permissions(token: str):
    permissions = jwt_bearer.client_manager.get_token_permissions(token)
    if permissions.llm < AccessRoles.GUEST:
            raise PermissionError("Insufficient permissions to access LLM service")

@bf_route.post("/get_models")
async def bf_get_models(token: str = Depends(jwt_bearer)) -> LLMGetModelsHttpResponse:
    _validate_permissions(token)
    user_id = jwt_bearer.client_manager.get_token_data(token).sub
    return mq_connector.get_brainforge_models(user_id)


@bf_route.post("/get_personas")
async def bf_get_personas(request: LLMGetPersonasHttpRequest,
                          token: str = Depends(jwt_bearer)) -> LLMGetPersonasHttpResponse:
    _validate_permissions(token)
    user_id = jwt_bearer.client_manager.get_token_data(token).sub
    return mq_connector.get_brainforge_model_personas(request.model_id, user_id)


@bf_route.post("/get_inference")
async def bf_get_inference(request: LLMGetInferenceHttpRequest,
                           token: str = Depends(jwt_bearer)) -> LLMResponse:
    _validate_permissions(token)
    user_id = jwt_bearer.client_manager.get_token_data(token).sub
    return mq_connector.get_brainforge_model_inference(request, user_id)


# TODO: OpenAI-compatible inference endpoint
