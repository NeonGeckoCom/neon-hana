import json
from time import time
from unittest import TestCase
from unittest.mock import patch

from fastapi.testclient import TestClient

from neon_data_models.models.user import User

_TEST_CONFIG = {
    "mq_default_timeout": 10,
    "access_token_ttl": 86400,  # 1 day
    "refresh_token_ttl": 604800,  # 1 week
    "requests_per_minute": 60,
    "auth_requests_per_minute": 60,
    "access_token_secret": "a800445648142061fc238d1f84e96200da87f4f9f784108ac90db8b4391b117b",
    "refresh_token_secret": "833d369ac73d883123743a44b4a7fe21203cffc956f4c8a99be6e71aafa8e1aa",
    "server_host": "0.0.0.0",
    "server_port": 8080,
    "fastapi_title": "Test Client Title",
    "fastapi_summary": "Test Client Summary",
    "stt_max_length_encoded": 500000,
    "tts_max_words": 128,
    "enable_email": True
}


class TestHanaApp(TestCase):
    test_app: TestClient = None
    tokens: dict = None

    @classmethod
    @patch("ovos_config.config.Configuration")
    @patch("neon_hana.mq_websocket_api.MQWebsocketAPI")
    def setUpClass(cls, ws_api, config):
        config.return_value = {"hana": _TEST_CONFIG}
        from neon_hana.app import create_app
        app = create_app(_TEST_CONFIG)
        cls.test_app = TestClient(app)

    @patch("neon_hana.mq_service_api.send_mq_request")
    def _get_tokens(self, send_request):
        valid_user = User(username="guest", password_hash="password")
        send_request.return_value = {"user": valid_user.model_dump(),
                                     "success": True}
        if not self.tokens:
            response = self.test_app.post("/auth/login",
                                          json={"username": "guest",
                                                "password": "password"})
            self.tokens = response.json()
            self.assertIn("access_token", self.tokens, self.tokens)
        return self.tokens

    def test_app_init(self):
        self.assertEqual(self.test_app.app.title, _TEST_CONFIG["fastapi_title"])
        self.assertEqual(self.test_app.app.summary,
                         _TEST_CONFIG["fastapi_summary"])

    @patch("neon_hana.mq_service_api.send_mq_request")
    def test_auth_login(self, send_request):
        valid_user = User(username="guest", password_hash="password")
        send_request.return_value = {"user": valid_user.model_dump(),
                                     "success": True}

        # Valid Login
        response = self.test_app.post("/auth/login",
                                      json={"username": valid_user.username,
                                            "password": valid_user.password_hash})
        response_data = response.json()
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response_data['username'], "guest")
        self.assertIsInstance(response_data['access_token'], str)
        self.assertIsInstance(response_data['refresh_token'], str)
        self.assertGreater(response_data['expiration'], time())

        # Invalid Login
        send_request.return_value = {"code": 404, "error": "User not found"}
        response = self.test_app.post("/auth/login",
                                      json={"username": valid_user.username,
                                            "password": valid_user.password_hash})
        self.assertEqual(response.status_code, 404, response.status_code)
        self.assertEqual(response.json()['detail'],
                         "User not found", response.text)

        # Invalid Request
        self.assertEqual(self.test_app.post("/auth/login").status_code, 422)
        self.assertEqual(self.test_app.post("/auth/login",
                                            json={"username": None}).status_code,
                         422)

    @patch("neon_hana.mq_service_api.send_mq_request")
    def test_auth_refresh(self, send_request):
        valid_user = User(username="guest", password_hash="password")
        send_request.return_value = {"user": valid_user.model_dump(),
                                     "success": True}

        valid_tokens = self._get_tokens()

        # Valid request
        response = self.test_app.post("/auth/refresh", json=valid_tokens)
        self.assertEqual(response.status_code, 200, response.text)
        response_data = response.json()
        self.assertNotEqual(response_data, valid_tokens)

        # Refresh with old tokens fails (mocked return from users service)
        send_request.return_value = {"code": 422,
                                     "detail": "Invalid token",
                                     "success": False}
        response = self.test_app.post("/auth/refresh", json=valid_tokens)
        self.assertEqual(response.status_code, 422, response.text)

        # TODO: Test with expired token

    @patch("neon_hana.mq_service_api.send_mq_request")
    def test_assist_get_stt(self, send_request):
        send_request.return_value = {"data": {"transcripts": ["test"],
                                              "parser_data": {"test": True}}}

        token = self._get_tokens()["access_token"]
        # Valid request
        response = self.test_app.post("/neon/get_stt",
                                      json={"encoded_audio": "MOCK_B64_AUDIO",
                                            "lang_code": "en-us"},
                                      headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json(), send_request.return_value['data'])

        # Invalid missing auth
        response = self.test_app.post("/neon/get_stt",
                                      json={"encoded_audio": "MOCK_B64_AUDIO",
                                            "lang_code": "en-us"})
        self.assertEqual(response.status_code, 403, response.text)

        # Invalid request
        self.assertEqual(self.test_app.post(
            "/neon/get_stt",
            headers={"Authorization": f"Bearer {token}"}).status_code,
                         422, response.text)

    @patch("neon_hana.mq_service_api.send_mq_request")
    def test_assist_get_tts(self, send_request):
        send_request.return_value = {"data": {
            "en-us": {"audio": {"female": "MOCK_B64_AUDIO"}}}}

        token = self._get_tokens()["access_token"]
        # Valid request
        response = self.test_app.post("/neon/get_tts",
                                      json={"to_speak": "test",
                                            "lang_code": "en-us"},
                                      headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()['encoded_audio'], "MOCK_B64_AUDIO")

        # Invalid missing auth
        response = self.test_app.post("/neon/get_tts",
                                      json={"to_speak": "test",
                                            "lang_code": "en-us"})
        self.assertEqual(response.status_code, 403, response.text)

        # Invalid request
        self.assertEqual(self.test_app.post(
            "/neon/get_tts",
            headers={"Authorization": f"Bearer {token}"}).status_code,
                         422, response.text)

    @patch("neon_hana.mq_service_api.send_mq_request")
    def test_assist_get_response(self, send_request):
        send_request.return_value = {
            "data": {"responses": {"en-us": {"sentence": "mock_response"}}},
            "context": {"session": {"new_session": True}}}

        token = self._get_tokens()["access_token"]
        # Valid request
        response = self.test_app.post("/neon/get_response",
                                      json={"utterance": "test",
                                            "lang_code": "en-us"},
                                      headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()['answer'], "mock_response")
        self.assertEqual(response.json()['lang_code'], "en-us")

        # Invalid missing auth
        response = self.test_app.post("/neon/get_response",
                                      json={"utterance": "test",
                                            "lang_code": "en-us"})
        self.assertEqual(response.status_code, 403, response.text)

        # Invalid request
        self.assertEqual(self.test_app.post(
            "/neon/get_response",
            headers={"Authorization": f"Bearer {token}"}).status_code,
                         422, response.text)

    @patch("neon_hana.mq_service_api.send_mq_request")
    def test_proxy_weather(self, send_request):
        send_request.return_value = {"status_code": 200,
                                     "content": json.dumps(
                                         {"lat": 47.6815,
                                          "lon": -122.2087,
                                          "timezone": "America/Los_Angeles",
                                          "timezone_offset": -28800,
                                          "current": {},
                                          "minutely": [],
                                          "hourly": [],
                                          "daily": []})}
        valid_request = {"lat": 47.6815,
                         "lon": -122.2087,
                         "unit": "metric"}

        token = self._get_tokens()["access_token"]
        # Valid request
        response = self.test_app.post("/proxy/weather",
                                      json=valid_request,
                                      headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json(),
                         json.loads(send_request.return_value['content']),
                         response.json())

        # Invalid missing auth
        response = self.test_app.post("/proxy/weather",
                                      json=valid_request)
        self.assertEqual(response.status_code, 403, response.text)

        # Invalid request
        self.assertEqual(self.test_app.post(
            "/proxy/weather",
            headers={"Authorization": f"Bearer {token}"}).status_code,
                         422, response.text)

    @patch("neon_hana.mq_service_api.send_mq_request")
    def test_proxy_stock_symbol(self, send_request):
        send_request.return_value = {"status_code": 200,
                                     "content": json.dumps(
                                         {"bestMatches": []})}
        valid_request = {"company": "microsoft",
                         "region": "United States"}

        token = self._get_tokens()["access_token"]
        # Valid request
        response = self.test_app.post("/proxy/stock/symbol",
                                      json=valid_request,
                                      headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()['bestMatches'],
                         json.loads(send_request.return_value['content'])['bestMatches'],
                         response.json())
        self.assertEqual(response.json()['provider'], "alpha_vantage")

        # Invalid missing auth
        response = self.test_app.post("/proxy/stock/symbol",
                                      json=valid_request)
        self.assertEqual(response.status_code, 403, response.text)

        # Invalid request
        self.assertEqual(self.test_app.post(
            "/proxy/stock/symbol",
            headers={"Authorization": f"Bearer {token}"}).status_code,
                         422, response.text)

        # TODO test region filtering

    @patch("neon_hana.mq_service_api.send_mq_request")
    def test_proxy_stock_quote(self, send_request):
        send_request.return_value = {"status_code": 200,
                                     "content": json.dumps(
                                         {"Global Quote": {"test": "True"}})}
        valid_request = {"symbol": "GOOG"}

        token = self._get_tokens()["access_token"]
        # Valid request
        response = self.test_app.post("/proxy/stock/quote",
                                      json=valid_request,
                                      headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()["Global Quote"],
                         json.loads(send_request.return_value['content'])["Global Quote"],
                         response.json())

        # Invalid missing auth
        response = self.test_app.post("/proxy/stock/quote",
                                      json=valid_request)
        self.assertEqual(response.status_code, 403, response.text)

        # Invalid request
        self.assertEqual(self.test_app.post(
            "/proxy/stock/quote",
            headers={"Authorization": f"Bearer {token}"}).status_code,
                         422, response.text)

    @patch("neon_hana.mq_service_api.send_mq_request")
    def test_proxy_geocode(self, send_request):
        send_request.return_value = {"status_code": 200,
                                     "content": json.dumps(
                                         {"place_id": 0,
                                          "licence": "test",
                                          "osm_type": "test",
                                          "osm_id": 0,
                                          "boundingbox": ["0", "0", "0", "0"],
                                          "lat": "47.6815",
                                          "lon": "-122.2087",
                                          "display_name": "test",
                                          "class": "amenity",
                                          "type": "post_office",
                                          "importance": 1.0,
                                          "alternate_results": []})}
        valid_request = {"address": "1100 Bellevue Way NE Bellevue, WA"}

        token = self._get_tokens()["access_token"]
        # Valid request
        response = self.test_app.post("/proxy/geolocation/geocode",
                                      json=valid_request,
                                      headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json(),
                         json.loads(send_request.return_value['content']),
                         response.json())

        # Invalid missing auth
        response = self.test_app.post("/proxy/geolocation/geocode",
                                      json=valid_request)
        self.assertEqual(response.status_code, 403, response.text)

        # Invalid request
        self.assertEqual(self.test_app.post(
            "/proxy/geolocation/geocode",
            headers={"Authorization": f"Bearer {token}"}).status_code,
                         422, response.text)

    @patch("neon_hana.mq_service_api.send_mq_request")
    def test_proxy_geocode_reverse(self, send_request):
        send_request.return_value = {"status_code": 200,
                                     "content": json.dumps(
                                         {"place_id": 0,
                                          "licence": "test",
                                          "osm_type": "test",
                                          "osm_id": 0,
                                          "boundingbox": ["0", "0", "0", "0"],
                                          "lat": "47.6815",
                                          "lon": "-122.2087",
                                          "display_name": "test",
                                          "address": {}})}

        valid_request = {"lat": 47.6815, "lon": -122.2087}

        token = self._get_tokens()["access_token"]
        # Valid request
        response = self.test_app.post("/proxy/geolocation/reverse",
                                      json=valid_request,
                                      headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json(),
                         json.loads(send_request.return_value['content']),
                         response.json())

        # Invalid missing auth
        response = self.test_app.post("/proxy/geolocation/reverse",
                                      json=valid_request)
        self.assertEqual(response.status_code, 403, response.text)

        # Invalid request
        self.assertEqual(self.test_app.post(
            "/proxy/geolocation/reverse",
            headers={"Authorization": f"Bearer {token}"}).status_code,
                         422, response.text)

    @patch("neon_hana.mq_service_api.send_mq_request")
    def test_proxy_wolfram(self, send_request):
        send_request.return_value = {"status_code": 200,
                                     "content": "answer"}
        valid_request = {"api": "spoken", "lat": 47.6815, "lon": -122.2087,
                         "query": "how far away is the moon"}

        token = self._get_tokens()["access_token"]
        # Valid request
        response = self.test_app.post("/proxy/wolframalpha",
                                      json=valid_request,
                                      headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json(),
                         {"answer": send_request.return_value['content']},
                         response.json())

        # Invalid missing auth
        response = self.test_app.post("/proxy/wolframalpha",
                                      json=valid_request)
        self.assertEqual(response.status_code, 403, response.text)

        # Invalid request
        self.assertEqual(self.test_app.post(
            "/proxy/wolframalpha",
            headers={"Authorization": f"Bearer {token}"}).status_code,
                         422, response.text)

    @patch("neon_hana.mq_service_api.send_mq_request")
    def test_backend_email(self, send_request):
        send_request.return_value = {"success": True}
        valid_request = {"recipient": "developers@neon.ai",
                         "subject": "API test",
                         "body": "This is a test.\nGenerated from OpenAPI.",
                         "attachments": {
                             "test.txt": "VGhpcyBpcyBhIHRlc3QgZmlsZQo="}}

        token = self._get_tokens()["access_token"]
        # Valid request
        response = self.test_app.post("/email",
                                      json=valid_request,
                                      headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200, response.text)

        # Invalid missing auth
        response = self.test_app.post("/email",
                                      json=valid_request)
        self.assertEqual(response.status_code, 403, response.text)

        # Invalid request
        self.assertEqual(self.test_app.post(
            "/email",
            headers={"Authorization": f"Bearer {token}"}).status_code,
                         422, response.text)

        # Valid request failed
        send_request.return_value = {"success": False,
                                     "error": "Something has failed"}
        response = self.test_app.post("/email",
                                      json=valid_request,
                                      headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 500, response.text)
        self.assertEqual(response.json()['detail'], "Something has failed")

        # TODO: Test disabled service

    @patch("neon_hana.mq_service_api.send_mq_request")
    def test_backend_metrics(self, send_request):
        send_request.return_value = {}
        valid_request = {"metric_name": "Unit Test",
                         "timestamp": str(time()),
                         "metric_data": {"test": True}}
        token = self._get_tokens()["access_token"]

        # Valid request
        response = self.test_app.post("/metrics/upload",
                                      json=valid_request,
                                      headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200, response.text)

        # Invalid missing auth
        response = self.test_app.post("/metrics/upload",
                                      json=valid_request)
        self.assertEqual(response.status_code, 403, response.text)

        # Invalid request
        self.assertEqual(self.test_app.post(
            "/metrics/upload",
            headers={"Authorization": f"Bearer {token}"}).status_code,
                         422, response.text)

    @patch("neon_hana.mq_service_api.send_mq_request")
    def test_backend_ccl(self, send_request):
        send_request.return_value = {"parsed_file": "MOCK_NCS_DATA"}
        valid_request = {"script": "MOCK_SCRIPT_DATA"}
        token = self._get_tokens()["access_token"]

        # Valid request
        response = self.test_app.post("/ccl/parse",
                                      json=valid_request,
                                      headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()['ncs'], "MOCK_NCS_DATA")

        # Invalid missing auth
        response = self.test_app.post("/ccl/parse",
                                      json=valid_request)
        self.assertEqual(response.status_code, 403, response.text)

        # Invalid request
        self.assertEqual(self.test_app.post(
            "/ccl/parse",
            headers={"Authorization": f"Bearer {token}"}).status_code,
                         422, response.text)

    @patch("neon_hana.mq_service_api.send_mq_request")
    def test_backend_coupons(self, send_request):
        send_request.return_value = {"success": True, "brands": [],
                                     "coupons": []}
        token = self._get_tokens()["access_token"]

        # Valid request
        response = self.test_app.post("/coupons",
                                      headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json(), send_request.return_value)

        # Invalid missing auth
        response = self.test_app.post("/coupons")
        self.assertEqual(response.status_code, 403, response.text)

    @patch("neon_hana.mq_service_api.send_mq_request")
    def test_llm(self, send_request):
        send_request.return_value = {"response": "MOCK_LLM_RESPONSE"}
        valid_request = {"query": "how are you?",
                         "history": [("user", "hello"),
                                     ("llm", "Hi, how can I help you today?")]}
        # Responses are lists instead of tuples because Pydantic will auto-cast
        # for JSON encoding
        valid_response = {"response": "MOCK_LLM_RESPONSE",
                          "history": [["user", "hello"],
                                      ["llm", "Hi, how can I help you today?"],
                                      ["user", "how are you?"],
                                      ["llm", "MOCK_LLM_RESPONSE"]]}
        token = self._get_tokens()["access_token"]
        # ChatGPT
        response = self.test_app.post("/llm/chatgpt",
                                      json=valid_request,
                                      headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), valid_response)

        # Fastchat
        response = self.test_app.post("/llm/fastchat",
                                      json=valid_request,
                                      headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), valid_response)

        # Claude
        response = self.test_app.post("/llm/claude",
                                      json=valid_request,
                                      headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), valid_response)

        # Palm
        response = self.test_app.post("/llm/palm",
                                      json=valid_request,
                                      headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), valid_response)

        # Invalid requests
        response = self.test_app.post("/llm/chatgpt",
                                      json=valid_request)
        self.assertEqual(response.status_code, 403, response.text)

        response = self.test_app.post("/llm/chatgpt",
                                      headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 422, response.text)

    def test_util_is_ipv4(self):
        from neon_hana.app.routers.util import _is_ipv4
        self.assertTrue(_is_ipv4("127.0.0.1"))
        self.assertTrue(_is_ipv4("10.0.0.10"))
        self.assertTrue(_is_ipv4("1.1.1.1"))
        self.assertFalse(_is_ipv4("ai.neon.api.1"))
        self.assertFalse(_is_ipv4("host.local"))
        self.assertFalse(_is_ipv4("localhost"))
        self.assertFalse(_is_ipv4("1.0.0.300"))

    def test_util_client_ip(self):
        response = self.test_app.get("/util/client_ip")
        self.assertEqual(response.text, "127.0.0.1")

    def test_util_headers(self):
        test_headers = {"X-Auth-Token": "Token",
                        "Authorization": "Test Auth",
                        "My Custom Header": "Value"}
        response = self.test_app.get("/util/headers", headers=test_headers)
        for key, val in test_headers.items():
            self.assertEqual(response.json()[key.lower()], val, response.json())

# TODO: Define node endpoint tests
