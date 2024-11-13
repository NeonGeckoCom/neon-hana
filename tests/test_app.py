from time import time
from unittest import TestCase
from unittest.mock import patch

from fastapi.testclient import TestClient

_TEST_CONFIG = {
    "mq_default_timeout": 10,
    "access_token_ttl": 86400,  # 1 day
    "refresh_token_ttl": 604800,  # 1 week
    "requests_per_minute": 60,
    "access_token_secret": "a800445648142061fc238d1f84e96200da87f4f9f784108ac90db8b4391b117b",
    "refresh_token_secret": "833d369ac73d883123743a44b4a7fe21203cffc956f4c8a99be6e71aafa8e1aa",
    "server_host": "0.0.0.0",
    "server_port": 8080,
    "fastapi_title": "Test Client Title",
    "fastapi_summary": "Test Client Summary",
    "stt_max_length_encoded": 500000,
    "tts_max_words": 128,
    "enable_email": False
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

    def _get_tokens(self):
        if not self.tokens:
            response = self.test_app.post("/auth/login",
                                          json={"username": "guest",
                                                "password": "password"})
            self.tokens = response.json()
        return self.tokens

    def test_app_init(self):
        self.assertEqual(self.test_app.app.title, _TEST_CONFIG["fastapi_title"])
        self.assertEqual(self.test_app.app.summary,
                         _TEST_CONFIG["fastapi_summary"])

    @patch("neon_hana.mq_service_api.send_mq_request")
    def test_auth_login(self, send_request):
        send_request.return_value = {}  # TODO: Define valid login

        # Valid Login
        response = self.test_app.post("/auth/login",
                                      json={"username": "guest",
                                            "password": "password"})
        response_data = response.json()
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response_data['username'], "guest")
        self.assertIsInstance(response_data['access_token'], str)
        self.assertIsInstance(response_data['refresh_token'], str)
        self.assertGreater(response_data['expiration'], time())

        # Invalid Login
        # TODO: Define invalid login request

        # Invalid Request
        self.assertEqual(self.test_app.post("/auth/login").status_code, 422)
        self.assertEqual(self.test_app.post("/auth/login",
                                            json={"username": None}).status_code,
                         422)

    @patch("neon_hana.mq_service_api.send_mq_request")
    def test_auth_refresh(self, send_request):
        send_request.return_value = {}  # TODO: Define valid refresh

        valid_tokens = self._get_tokens()

        # Valid request
        response = self.test_app.post("/auth/refresh", json=valid_tokens)
        self.assertEqual(response.status_code, 200, response.text)
        response_data = response.json()
        self.assertNotEqual(response_data, valid_tokens)

        # # TODO
        # # Refresh with old tokens fails
        # response = self.test_app.post("/auth/refresh", json=valid_tokens)
        # self.assertEqual(response.status_code, 422, response.text)

        # Valid request with new tokens
        response = self.test_app.post("/auth/refresh", json=response_data)
        self.assertEqual(response.status_code, 200, response.text)

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
        send_request.return_value = {}
        # TODO

    @patch("neon_hana.mq_service_api.send_mq_request")
    def test_proxy_stock_symbol(self, send_request):
        send_request.return_value = {}
        # TODO

    @patch("neon_hana.mq_service_api.send_mq_request")
    def test_proxy_stock_quote(self, send_request):
        send_request.return_value = {}
        # TODO

    @patch("neon_hana.mq_service_api.send_mq_request")
    def test_proxy_geocode(self, send_request):
        send_request.return_value = {}
        # TODO

    @patch("neon_hana.mq_service_api.send_mq_request")
    def test_proxy_geocode_reverse(self, send_request):
        send_request.return_value = {}
        # TODO

    @patch("neon_hana.mq_service_api.send_mq_request")
    def test_proxy_wolfram(self, send_request):
        send_request.return_value = {}
        # TODO

    @patch("neon_hana.mq_service_api.send_mq_request")
    def test_backend_email(self, send_request):
        send_request.return_value = {}
        # TODO

    @patch("neon_hana.mq_service_api.send_mq_request")
    def test_backend_metrics(self, send_request):
        send_request.return_value = {}
        # TODO

    @patch("neon_hana.mq_service_api.send_mq_request")
    def test_backend_ccl(self, send_request):
        send_request.return_value = {}
        # TODO

    @patch("neon_hana.mq_service_api.send_mq_request")
    def test_backend_coupons(self, send_request):
        send_request.return_value = {}
        # TODO

    @patch("neon_hana.mq_service_api.send_mq_request")
    def test_llm_chatgpt(self, send_request):
        send_request.return_value = {}
        # TODO

    @patch("neon_hana.mq_service_api.send_mq_request")
    def test_llm_fastchat(self, send_request):
        send_request.return_value = {}
        # TODO

    @patch("neon_hana.mq_service_api.send_mq_request")
    def test_llm_gemini(self, send_request):
        send_request.return_value = {}
        # TODO

    @patch("neon_hana.mq_service_api.send_mq_request")
    def test_llm_claude(self, send_request):
        send_request.return_value = {}
        # TODO

    @patch("neon_hana.mq_service_api.send_mq_request")
    def test_llm_palm(self, send_request):
        send_request.return_value = {}
        # TODO

    @patch("neon_hana.mq_service_api.send_mq_request")
    def test_util_client_ip(self, send_request):
        send_request.return_value = {}
        # TODO

    @patch("neon_hana.mq_service_api.send_mq_request")
    def test_util_headers(self, send_request):
        send_request.return_value = {}
        # TODO

# TODO: Define node endpoint tests
