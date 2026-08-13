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

from neon_hana.mq_service_api import APIError, AsyncMqServiceManager, MQServiceManager


class TestMqServiceApi(unittest.TestCase):
    def test_validate_api_proxy_response_missing_content_is_json_serializable(self):
        """Missing MQ content must raise APIError with JSON-serializable detail."""
        query_params = {"service": "open_weather_map", "lat": 47.6, "lon": -122.3}
        for cls in (AsyncMqServiceManager, MQServiceManager):
            with self.subTest(cls=cls.__name__):
                with self.assertRaises(APIError) as ctx:
                    cls._validate_api_proxy_response({}, query_params)
                exc = ctx.exception
                self.assertEqual(exc.status_code, 500)
                # FastAPI's HTTPException handler json.dumps()s detail; this is
                # the failure mode that previously surfaced as
                # "ValueError: Circular reference detected".
                json.dumps({"detail": exc.detail})
                self.assertEqual(exc.detail["error"],
                                 "No response content was received")
                self.assertEqual(exc.detail["raw_query"], query_params)
                self.assertNotIn("content", exc.detail["raw_response"])
