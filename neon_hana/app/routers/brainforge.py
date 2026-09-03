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

import asyncio
import json
from typing import AsyncIterator, Optional

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse, StreamingResponse
from neon_hana.app.dependencies import jwt_bearer, mq_connector
from neon_hana.mq_service_api import APIError

from neon_data_models.models.api.http.brainforge import (
    LLMGetModelsHttpResponse,
    LLMGetPersonasHttpRequest,
    LLMGetPersonasHttpResponse,
    LLMGetInferenceHttpRequest,
)
from neon_data_models.models.api.llm import LLMResponse
from neon_data_models.enum import AccessRoles


bf_route = APIRouter(
    prefix="/brainforge", tags=["llm"], dependencies=[Depends(jwt_bearer)]
)

_STREAM_END = object()


def _validate_permissions(token: str):
    permissions = jwt_bearer.client_manager.get_token_permissions(token)
    if permissions.llm < AccessRoles.GUEST:
        raise PermissionError("Insufficient permissions to access LLM service")


def _openai_error_response(
    message: str,
    status_code: int = 400,
    error_type: str = "invalid_request_error",
    param: Optional[str] = None,
    code: Optional[str] = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "message": message,
                "type": error_type,
                "param": param,
                "code": code,
            }
        },
    )


def _openai_error_from_backend(error: str) -> JSONResponse:
    lowered = error.lower()
    if "not found" in lowered:
        return _openai_error_response(
            error, status_code=404, param="model"
        )
    if any(token in lowered for token in ("missing", "expected", "validation")):
        return _openai_error_response(error, status_code=400)
    return _openai_error_response(error, status_code=500, error_type="api_error")


def _sse_data(payload: dict) -> str:
    return f"data: {json.dumps(payload)}\n\n"


@bf_route.post("/get_models")
async def bf_get_models(
    token: str = Depends(jwt_bearer),
) -> LLMGetModelsHttpResponse:
    _validate_permissions(token)
    user_id = jwt_bearer.client_manager.get_token_data(token).sub
    return await mq_connector.get_brainforge_models(user_id)


@bf_route.post("/get_personas")
async def bf_get_personas(
    request: LLMGetPersonasHttpRequest, token: str = Depends(jwt_bearer)
) -> LLMGetPersonasHttpResponse:
    _validate_permissions(token)
    user_id = jwt_bearer.client_manager.get_token_data(token).sub
    return await mq_connector.get_brainforge_model_personas(
        request.model_id, user_id
    )


@bf_route.post("/get_inference")
async def bf_get_inference(
    request: LLMGetInferenceHttpRequest, token: str = Depends(jwt_bearer)
) -> LLMResponse:
    _validate_permissions(token)
    user_id = jwt_bearer.client_manager.get_token_data(token).sub
    return await mq_connector.get_brainforge_model_inference(request, user_id)


# OpenAI-compatible endpoints
@bf_route.post("/openai/chat/completions")
async def openai_chat_completions(
    raw_request: Request,
    token: str = Depends(jwt_bearer),
):
    # Manually parse the raw request as FastAPI does not handle byte-encoding
    try:
        completion_kwargs = json.loads(await raw_request.body())
    except Exception:
        return _openai_error_response(
            "We could not parse the JSON body of your request"
        )
    if not isinstance(completion_kwargs, dict):
        return _openai_error_response(
            "Invalid type for 'request': expected an object"
        )
    if not completion_kwargs.get("model"):
        return _openai_error_response(
            "you must provide a model parameter", param="model"
        )

    _validate_permissions(token)
    user_id = jwt_bearer.client_manager.get_token_data(token).sub

    if completion_kwargs.get("stream"):
        queue = asyncio.Queue()
        loop = asyncio.get_running_loop()

        def on_response(response: dict):
            loop.call_soon_threadsafe(queue.put_nowait, response)

        async def request_completion():
            try:
                return await mq_connector.get_brainforge_model_completion(
                    completion_kwargs,
                    user_id,
                    stream_callback=on_response,
                )
            finally:
                loop.call_soon(queue.put_nowait, _STREAM_END)

        request_task = asyncio.create_task(request_completion())
        first = await queue.get()
        if first is _STREAM_END:
            try:
                await request_task
            except APIError as e:
                return _openai_error_from_backend(str(e.detail))
            return _openai_error_response(
                "Empty response from model",
                status_code=500,
                error_type="api_error",
            )
        if first.get("error"):
            if not request_task.done():
                request_task.cancel()
            return _openai_error_from_backend(str(first["error"]))

        async def remaining() -> AsyncIterator[str]:
            try:
                yield _sse_data(first["openai_response"])
                if not first.get("is_final", True):
                    while True:
                        response = await queue.get()
                        if response is _STREAM_END:
                            await request_task
                            break
                        if response.get("error"):
                            await request_task
                            break
                        yield _sse_data(response["openai_response"])
                        if response.get("is_final", True):
                            await request_task
                            break
                else:
                    await request_task
                yield "data: [DONE]\n\n"
            finally:
                if not request_task.done():
                    request_task.cancel()

        return StreamingResponse(
            remaining(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
            },
        )

    try:
        return await mq_connector.get_brainforge_model_completion(
            completion_kwargs, user_id
        )
    except APIError as e:
        return _openai_error_from_backend(str(e.detail))
