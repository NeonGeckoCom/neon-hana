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

import unittest
from uuid import uuid4


class TestClientManager(unittest.TestCase):
    from diana_services_api.auth.client_manager import ClientManager
    client_manager = ClientManager({})

    def test_check_auth_request(self):
        client_1 = str(uuid4())
        client_2 = str(uuid4())
        request_1 = {"username": "guest", "password": None,
                     "client_id": client_1}
        request_2 = {"username": "guest", "password": None,
                     "client_id": client_2}

        # Check simple auth
        auth_resp_1 = self.client_manager.check_auth_request(**request_1)
        self.assertEqual(self.client_manager.authorized_clients[client_1],
                         auth_resp_1)
        self.assertEqual(auth_resp_1['username'], 'guest')
        self.assertEqual(auth_resp_1['client_id'], client_1)

        # Check auth from different client
        auth_resp_2 = self.client_manager.check_auth_request(**request_2)
        self.assertNotEquals(auth_resp_1, auth_resp_2)
        self.assertEqual(self.client_manager.authorized_clients[client_2],
                         auth_resp_2)
        self.assertEqual(auth_resp_2['username'], 'guest')
        self.assertEqual(auth_resp_2['client_id'], client_2)

        # Check auth already authorized
        self.assertEqual(auth_resp_2,
                         self.client_manager.check_auth_request(**request_2))

    def test_validate_auth(self):
        valid_client = str(uuid4())
        invalid_client = str(uuid4())
        auth_response = self.client_manager.check_auth_request(
            username="valid", client_id=valid_client)['jwt_token']

        self.assertTrue(self.client_manager.validate_auth(auth_response))
        self.assertFalse(self.client_manager.validate_auth(invalid_client))
        self.client_manager.authorized_clients.pop(valid_client)
        self.assertFalse(self.client_manager.validate_auth(auth_response))
