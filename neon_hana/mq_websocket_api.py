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

from asyncio import run, get_event_loop
from time import time
from fastapi import WebSocket
from neon_iris.client import NeonAIClient
from ovos_bus_client.message import Message
from threading import RLock
from ovos_utils import LOG


class MQWebsocketAPI(NeonAIClient):
    def __init__(self, config: dict):
        """
        Creates an MQWebsocketAPI to serve multiple client WS connections.
        """
        mq_config = config.get("MQ") or dict()
        NeonAIClient.__init__(self, mq_config)
        self._sessions = dict()
        self._session_lock = RLock()
        self._client = "neon_node_websocket"

    def new_connection(self, ws: WebSocket, session_id: str):
        self._sessions[session_id] = {"session": {"session_id": session_id},
                                      "socket": ws}

    def get_session(self, session_id: str):
        with self._session_lock:
            sess = dict(self._sessions.get(session_id, {}).get("session"))
        return sess

    @property
    def user_config(self) -> dict:
        # TODO: Handle per-session config
        return super().user_config

    def _get_message_context(self, message):
        default_context = {"client_name": self.client_name,
                           "client": self._client,
                           "ident": str(time()),
                           "username": self.user_config['user']['username'],
                           "user_profiles": [self.user_config],
                           "neon_should_respond": True,
                           "timing": dict(),
                           "mq": {"routing_key": self.uid,
                                  "message_id": self.connection.
                                  create_unique_id()}}
        return {**message.context, **default_context}

    def _update_session_data(self, message):
        """
        Update the local session data from the latest response message's context
        """
        session_data = message.context.get('session')
        if session_data:
            session_id = session_data.get('session_id')
            with self._session_lock:
                self._sessions[session_id]['session'] = session_data

    def handle_client_input(self, data: dict, session_id: str):
        """
        Handle some client input
        """
        # Handle `Message.serialize` data sent over WS in addition to proper
        # dict representations
        data['msg_type'] = data.pop("type", data.get("msg_type"))
        message = Message(**data)
        message.context = self._get_message_context(message)
        message.context["session"] = self.get_session(session_id)
        # Send raw message, skipping any validation by iris
        self._send_message(message)

    def handle_klat_response(self, message: Message):
        self._update_session_data(message)
        run(self.send_to_client(message))
        LOG.debug(message.context.get("timing"))

    def handle_complete_intent_failure(self, message: Message):
        self._update_session_data(message)
        run(self.send_to_client(message))

    def handle_api_response(self, message: Message):
        if message.msg_type == "neon.audio_input.response":
            LOG.info(message.data.get("transcripts"))
        LOG.debug(message.context.get("timing"))

    def handle_error_response(self, message: Message):
        run(self.send_to_client(message))

    def clear_caches(self, message: Message):
        run(self.send_to_client(message))

    def clear_media(self, message: Message):
        run(self.send_to_client(message))

    def handle_alert(self, message: Message):
        run(self.send_to_client(message))

    async def send_to_client(self, message: Message):
        session_id = message.context["session"]["session_id"]
        await self._sessions[session_id]["socket"].send_text(message.serialize())

    def shutdown(self, *_, **__):
        loop = get_event_loop()
        loop.call_soon_threadsafe(loop.stop)
        LOG.info("Stopped Event Loop")
        super().shutdown()
