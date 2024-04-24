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
from time import time
from uuid import uuid4

from fastapi import HTTPException


class TestClientManager(unittest.TestCase):
    from neon_hana.auth.client_manager import ClientManager
    client_manager = ClientManager({"access_token_secret": "a800445648142061fc238d1f84e96200da87f4f9f784108ac90db8b4391b117b",
                                    "refresh_token_secret": "a800445648142061fc238d1f84e96200da87f4f9f784108ac90db8b4391b117b",
                                    "disable_auth": False})

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

        # TODO: Test permissions

        # Check auth already authorized
        self.assertEqual(auth_resp_2,
                         self.client_manager.check_auth_request(**request_2))

    def test_validate_auth(self):
        valid_client = str(uuid4())
        invalid_client = str(uuid4())
        auth_response = self.client_manager.check_auth_request(
            username="valid", client_id=valid_client)['access_token']

        self.assertTrue(self.client_manager.validate_auth(auth_response,
                                                          "127.0.0.1"))
        self.assertFalse(self.client_manager.validate_auth(invalid_client,
                                                           "127.0.0.1"))

        expired_token = self.client_manager._create_tokens(
            {"client_id": invalid_client, "username": "test",
             "password": "test", "expire": time(),
             "permissions": {}})['access_token']
        self.assertFalse(self.client_manager.validate_auth(expired_token,
                                                           "127.0.0.1"))

        self.client_manager._rpm = 1
        self.assertTrue(self.client_manager.validate_auth(auth_response,
                                                          "192.168.1.2"))
        with self.assertRaises(HTTPException) as e:
            self.client_manager.validate_auth(auth_response, "192.168.1.2")
        self.assertEqual(e.exception.status_code, 429)

    def test_check_refresh_request(self):
        valid_client = str(uuid4())
        tokens = self.client_manager._create_tokens({"client_id": valid_client,
                                                     "username": "test",
                                                     "password": "test",
                                                     "expire": time(),
                                                     "permissions": {}})
        self.assertEqual(tokens['client_id'], valid_client)

        # Test invalid refresh token
        with self.assertRaises(HTTPException) as e:
            self.client_manager.check_refresh_request(tokens['access_token'],
                                                      valid_client,
                                                      valid_client)
        self.assertEqual(e.exception.status_code, 400)

        # Test incorrect access token
        with self.assertRaises(HTTPException) as e:
            self.client_manager.check_refresh_request(tokens['refresh_token'],
                                                      tokens['refresh_token'],
                                                      valid_client)
        self.assertEqual(e.exception.status_code, 403)

        # Test invalid client_id
        with self.assertRaises(HTTPException) as e:
            self.client_manager.check_refresh_request(tokens['access_token'],
                                                      tokens['refresh_token'],
                                                      str(uuid4()))
        self.assertEqual(e.exception.status_code, 403)

        # Test valid refresh
        valid_refresh = self.client_manager.check_refresh_request(
            tokens['access_token'], tokens['refresh_token'],
            tokens['client_id'])
        self.assertEqual(valid_refresh['client_id'], tokens['client_id'])
        self.assertNotEqual(valid_refresh['access_token'],
                            tokens['access_token'])
        self.assertNotEqual(valid_refresh['refresh_token'],
                            tokens['refresh_token'])

        # Test expired refresh token
        real_refresh = self.client_manager._refresh_token_lifetime
        self.client_manager._refresh_token_lifetime = 0
        tokens = self.client_manager._create_tokens({"client_id": valid_client,
                                                     "username": "test",
                                                     "password": "test",
                                                     "expire": time(),
                                                    "permissions": {}})
        with self.assertRaises(HTTPException) as e:
            self.client_manager.check_refresh_request(tokens['access_token'],
                                                      tokens['refresh_token'],
                                                      tokens['client_id'])
        self.assertEqual(e.exception.status_code, 401)
        self.client_manager._refresh_token_lifetime = real_refresh

    def test_get_permissions(self):
        from neon_hana.auth.permissions import ClientPermissions

        node_user = "node_test"
        rest_user = "rest_user"
        self.client_manager._node_username = node_user
        self.client_manager._node_password = node_user

        rest_resp = self.client_manager.check_auth_request(rest_user, rest_user)
        node_resp = self.client_manager.check_auth_request(node_user, node_user,
                                                           node_user)
        node_fail = self.client_manager.check_auth_request("node_fail",
                                                           node_user, rest_user)

        rest_cid = rest_resp['client_id']
        node_cid = node_resp['client_id']
        fail_cid = node_fail['client_id']

        permissive = ClientPermissions(True, True, True)
        no_node = ClientPermissions(True, True, False)
        no_perms = ClientPermissions(False, False, False)

        # Auth disabled, returns all True
        self.client_manager._disable_auth = True
        self.assertEqual(self.client_manager.get_permissions(rest_cid),
                         permissive)
        self.assertEqual(self.client_manager.get_permissions(node_cid),
                         permissive)
        self.assertEqual(self.client_manager.get_permissions(rest_cid),
                         permissive)
        self.assertEqual(self.client_manager.get_permissions(fail_cid),
                         permissive)
        self.assertEqual(self.client_manager.get_permissions("fake_user"),
                         permissive)

        # Auth enabled
        self.client_manager._disable_auth = False
        self.assertEqual(self.client_manager.get_permissions(rest_cid), no_node)
        self.assertEqual(self.client_manager.get_permissions(node_cid),
                         permissive)
        self.assertEqual(self.client_manager.get_permissions(fail_cid), no_node)
        self.assertEqual(self.client_manager.get_permissions("fake_user"),
                         no_perms)

    def test_client_permissions(self):
        from neon_hana.auth.permissions import ClientPermissions
        default_perms = ClientPermissions()
        restricted_perms = ClientPermissions(False, False, False)
        permissive_perms = ClientPermissions(True, True, True)
        self.assertIsInstance(default_perms.as_dict(), dict)
        for v in default_perms.as_dict().values():
            self.assertIsInstance(v, bool)
        self.assertIsInstance(restricted_perms.as_dict(), dict)
        self.assertFalse(any([v for v in restricted_perms.as_dict().values()]))
        self.assertIsInstance(permissive_perms.as_dict(), dict)
        self.assertTrue(all([v for v in permissive_perms.as_dict().values()]))
