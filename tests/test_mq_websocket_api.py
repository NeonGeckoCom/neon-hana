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

import json
import unittest

from unittest.mock import AsyncMock, MagicMock, patch

from neon_utils.socket_utils import dict_to_b64
from ovos_bus_client.message import Message

from neon_hana.mq_websocket_api import MQWebsocketAPI


TEST_SESSION = "node-test"

VALID_HELLO = {"msg_type": "node.hello",
               "data": {"node_id": TEST_SESSION,
                        "node_name": "Kitchen Phone",
                        "capabilities": {"launch_camera_app": True,
                                         "launch_sms_app": False}}}


def _make_api() -> MQWebsocketAPI:
    with patch("neon_hana.mq_websocket_api.NeonAIClient.__init__",
               return_value=None):
        api = MQWebsocketAPI({})
    api.client_name = "test_client"
    api._uid = "test-uid"
    api._connection = MagicMock()
    api._connection.create_unique_id.return_value = "test-mid"
    api._send_message = MagicMock()
    return api


def _seed_session(api: MQWebsocketAPI, session_id: str = TEST_SESSION,
                  site_id: str = "kitchen"):
    socket = MagicMock()
    socket.send_text = AsyncMock()
    api._sessions[session_id] = {
        "session": {"session_id": session_id, "site_id": site_id},
        "socket": socket,
        "user": {"user": {"username": "tester"}}}
    return socket


class TestNodeHello(unittest.TestCase):
    def test_hello_caches_snapshot(self):
        api = _make_api()
        _seed_session(api)
        api.handle_client_input(dict(VALID_HELLO), TEST_SESSION)
        cached = api._sessions[TEST_SESSION]["node"]
        self.assertEqual(cached["node_id"], TEST_SESSION)
        self.assertEqual(cached["node_name"], "Kitchen Phone")
        self.assertEqual(cached["capabilities"],
                         {"launch_camera_app": True, "launch_sms_app": False})
        # The hello is still forwarded to the bus
        api._send_message.assert_called_once()

    def test_hello_session_identity_is_authoritative(self):
        api = _make_api()
        _seed_session(api)
        hello = {"msg_type": "node.hello",
                 "data": {**VALID_HELLO["data"], "node_id": "someone-else"}}
        api.handle_client_input(hello, TEST_SESSION)
        # The token-derived session ID wins over the self-reported node_id
        self.assertEqual(api._sessions[TEST_SESSION]["node"]["node_id"],
                         TEST_SESSION)

    def test_invalid_hello_ignored(self):
        api = _make_api()
        _seed_session(api)
        for bad_data in ({},  # missing node_id
                         {"node_id": TEST_SESSION,
                          "node_name": "x" * 129}):  # name over cap
            api.handle_client_input({"msg_type": "node.hello",
                                     "data": bad_data}, TEST_SESSION)
            self.assertNotIn("node", api._sessions[TEST_SESSION])

    def test_hello_updates_on_repeat(self):
        api = _make_api()
        _seed_session(api)
        api.handle_client_input(dict(VALID_HELLO), TEST_SESSION)
        renamed = {"msg_type": "node.hello",
                   "data": {**VALID_HELLO["data"], "node_name": "Den Phone"}}
        api.handle_client_input(renamed, TEST_SESSION)
        self.assertEqual(api._sessions[TEST_SESSION]["node"]["node_name"],
                         "Den Phone")

    @staticmethod
    def _hello_acks(socket) -> list:
        return [m for m in
                (json.loads(c.args[0])
                 for c in socket.send_text.call_args_list)
                if m["type"] == "node.hello.response"]

    def test_hello_acknowledged_with_normalized_snapshot(self):
        api = _make_api()
        socket = _seed_session(api)
        api.handle_client_input(dict(VALID_HELLO), TEST_SESSION)
        ack = self._hello_acks(socket)[0]
        self.assertEqual(ack["data"]["status"], "success")
        self.assertEqual(ack["data"]["node"]["node_id"], TEST_SESSION)
        self.assertEqual(ack["data"]["node"]["node_name"], "Kitchen Phone")
        self.assertEqual(ack["data"]["node"]["capabilities"],
                         {"launch_camera_app": True, "launch_sms_app": False})

    def test_hello_ack_echoes_session_identity_not_claimed_id(self):
        # The ack reports what context.node will actually carry, so a Node
        # that claimed a different node_id learns the hub overrode it
        api = _make_api()
        socket = _seed_session(api)
        hello = {"msg_type": "node.hello",
                 "data": {**VALID_HELLO["data"], "node_id": "someone-else"}}
        api.handle_client_input(hello, TEST_SESSION)
        ack = self._hello_acks(socket)[0]
        self.assertEqual(ack["data"]["node"]["node_id"], TEST_SESSION)

    def test_rejected_hello_gets_error_response(self):
        # A rejection is otherwise invisible to the Node -- it only shows up
        # later as capability gating silently doing nothing
        api = _make_api()
        socket = _seed_session(api)
        api.handle_client_input({"msg_type": "node.hello", "data": {}},
                                TEST_SESSION)
        ack = self._hello_acks(socket)[0]
        self.assertEqual(ack["data"]["status"], "error")
        self.assertIn("node_id", ack["data"]["error"]["message"])
        self.assertNotIn("node", ack["data"])


class TestNodeContextEnrichment(unittest.TestCase):
    def test_context_includes_node_after_hello(self):
        api = _make_api()
        _seed_session(api)
        api.handle_client_input(dict(VALID_HELLO), TEST_SESSION)
        context = api._get_message_context(
            Message("neon.audio_input", {}, {}), TEST_SESSION)
        self.assertEqual(context["node"],
                         {"node_id": TEST_SESSION,
                          "node_name": "Kitchen Phone",
                          "site_id": "kitchen",
                          "capabilities": {"launch_camera_app": True,
                                           "launch_sms_app": False}})

    def test_context_without_hello_has_no_node(self):
        api = _make_api()
        _seed_session(api)
        context = api._get_message_context(
            Message("neon.audio_input", {}, {}), TEST_SESSION)
        self.assertNotIn("node", context)


class TestInvokeNativeDispatch(unittest.TestCase):
    def _invoke_body(self, session_id: str = TEST_SESSION) -> bytes:
        return dict_to_b64(
            {"msg_type": "node.invoke_native",
             "data": {"action": "launch_camera_app"},
             "context": {"session": {"session_id": session_id}}})

    def test_invoke_native_routed_to_client(self):
        api = _make_api()
        socket = _seed_session(api)
        channel = MagicMock()
        method = MagicMock()
        method.delivery_tag = 1
        api.handle_neon_response(channel, method, None, self._invoke_body())
        channel.basic_ack.assert_called_once_with(delivery_tag=1)
        socket.send_text.assert_called_once()
        # `Message.serialize` uses `type` on the wire (see handle_client_input)
        sent = json.loads(socket.send_text.call_args[0][0])
        self.assertEqual(sent["type"], "node.invoke_native")
        self.assertEqual(sent["data"]["action"], "launch_camera_app")

    def test_other_messages_delegate_to_iris(self):
        api = _make_api()
        _seed_session(api)
        body = dict_to_b64({"msg_type": "klat.response", "data": {},
                            "context": {"session":
                                        {"session_id": TEST_SESSION}}})
        channel = MagicMock()
        method = MagicMock()
        with patch("neon_hana.mq_websocket_api.NeonAIClient."
                   "handle_neon_response") as delegate:
            api.handle_neon_response(channel, method, None, body)
        delegate.assert_called_once_with(channel, method, None, body)
        channel.basic_ack.assert_not_called()

    def test_invoke_native_unknown_session_logged_not_raised(self):
        api = _make_api()
        message = Message("node.invoke_native",
                          {"action": "launch_camera_app"},
                          {"session": {"session_id": "node-gone"}})
        # Must not raise; the skill's own timeout handles the failure path
        api.handle_node_invoke_native(message)


class TestInvokeNativeResponsePassthrough(unittest.TestCase):
    def test_response_forwarded_to_bus(self):
        api = _make_api()
        _seed_session(api)
        api.handle_client_input(
            {"msg_type": "node.invoke_native.response",
             "data": {"action": "launch_camera_app", "status": "success"},
             "context": {}}, TEST_SESSION)
        api._send_message.assert_called_once()
        forwarded = api._send_message.call_args[0][0]
        self.assertEqual(forwarded.msg_type, "node.invoke_native.response")
        self.assertEqual(forwarded.data["status"], "success")
        self.assertEqual(forwarded.context["session"]["session_id"],
                         TEST_SESSION)


if __name__ == '__main__':
    unittest.main()
