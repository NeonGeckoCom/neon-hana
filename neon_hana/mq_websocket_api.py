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
from os import makedirs
from queue import Queue
from time import time, sleep
from typing import Optional
from fastapi import WebSocket
from neon_iris.client import NeonAIClient
from ovos_bus_client.message import Message
from threading import RLock
from ovos_utils import LOG


class ClientNotKnown(RuntimeError):
    """
    Exception raised when a client tries to do something before authenticating
    """


class MQWebsocketAPI(NeonAIClient):
    def __init__(self, config: dict):
        """
        Creates an MQWebsocketAPI to serve multiple client WS connections.
        """
        mq_config = config.get("MQ") or dict()
        config_dir = "/tmp/hana"
        makedirs(config_dir, exist_ok=True)
        NeonAIClient.__init__(self, mq_config, config_dir=config_dir)
        self._sessions = dict()
        self._session_lock = RLock()
        self._client = "neon_node_websocket"

    def new_connection(self, ws: WebSocket, session_id: str):
        """
        Record a new client connection to associate the WebSocket with the
        session_id for response routing.
        @param ws: Client WebSocket object
        @param session_id: Session ID of the client
        """
        self._sessions[session_id] = {"session": {"session_id": session_id},
                                      "socket": ws,
                                      "user": self.user_config}

    def new_stream(self, ws: WebSocket, session_id: str):
        """
        Establish a new streaming connection, associated with an existing session.
        @param ws: Client WebSocket that handles byte audio
        @param session_id: Session ID the websocket is associated with
        """
        timeout = time() + 5
        while session_id not in self._sessions and time() < timeout:
            # Handle problem clients that don't explicitly wait for the Node WS
            # to connect before starting a stream
            sleep(1)
        with self._session_lock:
            if session_id not in self._sessions:
                raise ClientNotKnown(f"Stream cannot be established for {session_id}")
            from neon_hana.streaming_client import RemoteStreamHandler, StreamMicrophone
            if not self._sessions[session_id].get('stream'):
                LOG.info(f"starting stream for session {session_id}")
                audio_queue = Queue()
                stream = RemoteStreamHandler(StreamMicrophone(audio_queue), session_id,
                                             input_audio_callback=self.handle_client_input,
                                             ww_callback=self.handle_ww_detected,
                                             client_socket=ws)
                self._sessions[session_id]['stream'] = stream
                try:
                    stream.start()
                except RuntimeError:
                    pass

    def end_session(self, session_id: str):
        """
        End a client connection upon WS disconnection
        """
        with self._session_lock:
            session: Optional[dict] = self._sessions.pop(session_id, None)
        if not session:
            LOG.error(f"Ended session is not established {session_id}")
            return
        stream = session.get('stream')
        if stream:
            stream.shutdown()
            stream.join()
            LOG.info(f"Ended stream handler for: {session_id}")

    def get_session(self, session_id: str) -> dict:
        """
        Get the latest session context for the given session_id.
        @param session_id: Session ID to get context for
        @return: dict context for the given session_id (may be empty)
        """
        with self._session_lock:
            sess = dict(self._sessions.get(session_id, {}).get("session", {}))
        return sess

    def get_user_config(self, session_id: str) -> dict:
        """
        Get a dict user configuration for the given session_id
        @param session_id: Session to get user configuration for
        @return: dict user configuration
        """
        with self._session_lock:
            config = dict(self._sessions.get(session_id, {}).get("user") or
                          self.user_config)
        return config

    def _get_message_context(self, message: Message, session_id: str) -> dict:
        """
        Build message context for a Node input message.
        @param message: Input message to include context from
        @param session_id: Session ID associated with the message
        @return: dict context for this input
        """
        user_config = self.get_user_config(session_id)
        default_context = {"client_name": self.client_name,
                           "client": self._client,
                           "ident": str(time()),
                           "username": user_config['user']['username'],
                           "user_profiles": [user_config],
                           "neon_should_respond": True,
                           "timing": dict(),
                           "mq": {"routing_key": self.uid,
                                  "message_id": self.connection.
                                  create_unique_id()}}
        return {**message.context, **default_context}

    def _update_session_data(self, message: Message):
        """
        Update the local session data and user profile from the latest response
        message's context.
        @param message: Response message containing updated context
        """
        session_data = message.context.get('session')
        if session_data:
            user_config = message.context.get('user_profiles', [None])[0]
            session_id = session_data.get('session_id')
            with self._session_lock:
                self._sessions[session_id]['session'] = session_data
                if user_config:
                    self._sessions[session_id]['user'] = user_config

    def handle_audio_input_stream(self, audio: bytes, session_id: str):
        self._sessions[session_id]['stream'].mic.queue.put(audio)

    def handle_ww_detected(self, ww_context: dict, session_id: str):
        session = self.get_session(session_id)
        message = Message("neon.ww_detected", ww_context,
                          {"session": session})
        run(self.send_to_client(message))

    def handle_client_input(self, data: dict, session_id: str):
        """
        Handle some client input data.
        @param data: Decoded input from client WebSocket
        @param session_id: Session ID associated with the client connection
        """
        # Handle `Message.serialize` data sent over WS in addition to proper
        # dict representations
        data['msg_type'] = data.pop("type", data.get("msg_type"))
        message = Message(**data)
        message.context = self._get_message_context(message, session_id)
        message.context["session"] = self.get_session(session_id)
        # Send raw message, skipping any validation by iris
        self._send_message(message)

    def handle_klat_response(self, message: Message):
        """
        Handle a Neon text+audio response to a user input.
        @param message: `klat.response` message from Neon
        """
        try:
            self._update_session_data(message)
            run(self.send_to_client(message))
            session_id = message.context.get('session', {}).get('session_id')
            if stream := self._sessions.get(session_id, {}).get('stream'):
                LOG.info("Stream response audio")
                stream.on_response_audio(message.data)
            LOG.debug(message.context.get("timing"))
        except Exception as e:
            LOG.exception(e)

    def handle_complete_intent_failure(self, message: Message):
        """
        Handle a Neon error response to a user input.
        @param message: `complete.intent.failure` message from Neon
        """
        self._update_session_data(message)
        run(self.send_to_client(message))

    def handle_api_response(self, message: Message):
        """
        Handle a Neon API response to an input.
        @param message: `<msg_type>.response` message from Neon
        """
        if message.msg_type == "neon.audio_input.response":
            LOG.info(message.data.get("transcripts"))
        LOG.debug(message.context.get("timing"))
        run(self.send_to_client(message))

    def handle_error_response(self, message: Message):
        """
        Handle an MQ error response to a user input.
        @param message: `klat.error` response message
        """
        run(self.send_to_client(message))

    def clear_caches(self, message: Message):
        """
        Handle a Neon request to clear cached data.
        @param message: `neon.clear_data` message from Neon
        """
        run(self.send_to_client(message))

    def clear_media(self, message: Message):
        """
        Handle a Neon request to clear media data.
        @param message: `neon.clear_data` message from Neon
        """
        run(self.send_to_client(message))

    def handle_alert(self, message: Message):
        """
        Handle an expired alert from Neon.
        @param message: `neon.alert_expired` message from Neon
        """
        run(self.send_to_client(message))

    async def send_to_client(self, message: Message):
        """
        Asynchronously forward a message from Neon/MQ to a WebSocket client.
        @param message: Message to forward to a WebSocket client
        """
        # TODO: Drop context?
        session_id = message.context["session"]["session_id"]
        await self._sessions[session_id]["socket"].send_text(message.serialize())

    def shutdown(self, *_, **__):
        """
        Shutdown the event loop and prepare this object for destruction.
        """
        loop = get_event_loop()
        loop.call_soon_threadsafe(loop.stop)
        LOG.info("Stopped Event Loop")
        super().shutdown()
