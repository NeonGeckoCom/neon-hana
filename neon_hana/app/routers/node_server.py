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

from asyncio import Event
from signal import signal, SIGINT
from typing import Optional, Union

from fastapi import APIRouter, WebSocket, HTTPException, Request
from starlette.websockets import WebSocketDisconnect

from neon_hana.app.dependencies import config, client_manager
from neon_hana.mq_websocket_api import MQWebsocketAPI

from neon_hana.schema.node_v1 import (NodeAudioInput, NodeGetStt,
                                      NodeGetTts, NodeKlatResponse,
                                      NodeAudioInputResponse,
                                      NodeGetSttResponse,
                                      NodeGetTtsResponse)
node_route = APIRouter(prefix="/node", tags=["node"])

socket_api = MQWebsocketAPI(config)
signal(SIGINT, socket_api.shutdown)


@node_route.websocket("/v1")
async def node_v1_endpoint(websocket: WebSocket, token: str):
    client_id = client_manager.get_client_id(token)
    if not client_manager.validate_auth(token, client_id):
        raise HTTPException(status_code=403,
                            detail="Invalid or expired token.")
    if not client_manager.get_permissions(client_id).node:
        raise HTTPException(status_code=401,
                            detail=f"Client not authorized for node access "
                                   f"({client_id})")
    await websocket.accept()
    disconnect_event = Event()

    socket_api.new_connection(websocket, client_id)
    while not disconnect_event.is_set():
        try:
            client_in: dict = await websocket.receive_json()
            socket_api.handle_client_input(client_in, client_id)
        except WebSocketDisconnect:
            disconnect_event.set()


@node_route.websocket("/v1/stream")
async def node_v1_endpoint(websocket: WebSocket, token: str):
    """
    Endpoint to handle a stream of raw audio bytes. A client using this endpoint
    must first establish a connection to the `/v1` endpoint.
    """
    client_id = client_manager.get_client_id(token)
    if not socket_api.get_session(client_id):
        raise HTTPException(status_code=401,
                            detail=f"Client not known ({client_id})")
    await websocket.accept()
    disconnect_event = Event()

    while not disconnect_event.is_set():
        try:
            client_in: bytes = await websocket.receive_bytes()
            socket_api.handle_audio_stream(client_in, client_id)
        except WebSocketDisconnect:
            disconnect_event.set()


@node_route.get("/v1/doc")
async def node_v1_doc(_: Optional[Union[NodeAudioInput, NodeGetStt,
                                        NodeGetTts]]) -> \
        Optional[Union[NodeKlatResponse, NodeAudioInputResponse,
                       NodeGetSttResponse, NodeGetTtsResponse]]:
    pass
