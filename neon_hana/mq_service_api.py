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

from time import time
from typing import Optional, Dict, Any, List
from uuid import uuid4
from fastapi import HTTPException

from neon_hana.schema.node_model import NodeData
from neon_hana.schema.user_profile import UserProfile
from neon_mq_connector.utils.client_utils import send_mq_request


class APIError(HTTPException):
    """
    Exception class representing errors in getting responses from the MQ API
    """


class MQServiceManager:
    def __init__(self, config: dict):
        self.mq_default_timeout = config.get('mq_default_timeout', 10)
        self.mq_cliend_id = config.get('mq_client_id') or str(uuid4())
        self.stt_max_length = config.get('stt_max_length_encoded') or 500000
        self.tts_max_words = config.get('tts_max_words') or 128
        self.email_enabled = config.get('enable_email')
        self.sessions_by_id = dict()

    @staticmethod
    def _validate_api_proxy_response(response: dict, query_params: dict):
        if response['status_code'] == 200:
            try:
                resp = json.loads(response['content'])
                if isinstance(resp, dict):
                    return resp
                # Reverse Geocode API returns a list; reformat that to a dict
                if isinstance(resp, list):
                    return {**resp.pop(0),
                            **{"alternate_results": resp}}
                if query_params.get('service') == "alpha_vantage":
                    if query_params.get("region"):
                        filtered = [
                            stock for stock in response.get("bestMatches")
                            if stock.get("4. region") == query_params["region"]]
                        response['bestMatches'] = filtered

                # TODO: Re-format Stock returns
            except json.JSONDecodeError:
                resp = response['content']
            # Wolfram Spoken API returns a string; reformat that to a dict
            if isinstance(resp, str):
                return {"answer": resp}
        code = response['status_code'] if response['status_code'] > 200 else 500
        raise APIError(status_code=code, detail=response['content'])

    def get_session(self, node_data: NodeData) -> dict:
        """
        Get a serialized Session object for the specified Node.
        @param node_data: NodeData received from client
        @returns: Serialized session, possibly cached from previous a response
        """
        session_id = node_data.device_id
        self.sessions_by_id.setdefault(session_id,
                                       {"session_id": session_id,
                                        "site_id": node_data.location.site_id})
        return self.sessions_by_id[session_id]

    def query_api_proxy(self, service_name: str, query_params: dict,
                        timeout: int = 10):
        query_params['service'] = service_name
        response = send_mq_request("/neon_api", query_params, "neon_api_input",
                                   "neon_api_output", timeout)
        return self._validate_api_proxy_response(response, query_params)

    def query_llm(self, llm_name: str, query: str, history: List[tuple]):
        response = send_mq_request("/llm", {"query": query,
                                            "history": history},
                                   f"{llm_name}_input",
                                   response_queue=f"{llm_name}_"
                                                  f"{self.mq_cliend_id}")
        response = response.get('response') or ""
        history.append(("user", query))
        history.append(("llm", response))
        return {"response": response,
                "history": history}

    def send_email(self, recipient: str, subject: str, body: str,
                   attachments: Optional[Dict[str, str]]):
        if not self.email_enabled:
            raise APIError(status_code=503, detail="Email service disabled")
        request_data = {"recipient": recipient,
                        "subject": subject,
                        "body": body,
                        "attachments": attachments}
        response = send_mq_request("/neon_emails", request_data,
                                   "neon_emails_input")
        if not response.get("success"):
            raise APIError(status_code=500, detail="Email failed to send")

    def upload_metric(self, metric_name: str, timestamp: str,
                      metric_data: Dict[str, Any]):
        metric_data = {**{"name": metric_name, "timestamp": timestamp},
                       **metric_data}
        send_mq_request("/neon_metrics", metric_data, "neon_metrics_input",
                        expect_response=False)

    def parse_ccl_script(self, script: str, metadata: Dict[str, Any]):
        try:
            response = send_mq_request("/neon_script_parser",
                                       {"text": script, "metadata": metadata},
                                       "neon_script_parser_input",
                                       "neon_script_parser_output",
                                       self.mq_default_timeout)
            return {"ncs": response['parsed_file']}
        except TimeoutError as e:
            raise APIError(status_code=500, detail=repr(e))

    def get_coupons(self):
        try:
            response = send_mq_request("/neon_coupons", {},
                                       "neon_coupons_input",
                                       "neon_coupons_output",
                                       self.mq_default_timeout)
            return response
        except TimeoutError as e:
            raise APIError(status_code=500, detail=repr(e))

    def get_stt(self, encoded_audio: str, lang_code: str):
        if 0 < self.stt_max_length < len(encoded_audio):
            raise APIError(status_code=400,
                           detail=f"Audio exceeds maximum encoded length of "
                                  f"{self.stt_max_length}")
        request_data = {"msg_type": "neon.get_stt",
                                    "data": {"audio_data": encoded_audio,
                                             "utterances": [""],  # TODO: Compat
                                             "lang": lang_code},
                                    "context": {"source": "hana",
                                                "ident": f"{self.mq_cliend_id}"
                                                         f"{time()}"}}
        response = send_mq_request("/neon_chat_api", request_data,
                                   "neon_chat_api_request",
                                   timeout=self.mq_default_timeout)
        return response['data']

    def get_tts(self, to_speak: str, lang_code: str, gender: str):
        if 0 < self.tts_max_words < len(to_speak.split()):
            raise APIError(status_code=400,
                           detail=f"Text exceeds maximum word count of "
                                  f"{self.tts_max_words}")
        request_data = {"msg_type": "neon.get_tts",
                        "data": {"text": to_speak,
                                 "utterance": "",  # TODO: Compat
                                 "speaker": {"name": "Neon",
                                             "gender": gender,
                                             "lang": lang_code},
                                 "lang": lang_code},
                        "context": {"source": "hana",
                                    "ident": f"{self.mq_cliend_id}{time()}"}}
        response = send_mq_request("/neon_chat_api", request_data,
                                   "neon_chat_api_request",
                                   timeout=self.mq_default_timeout)
        audio = response['data'][lang_code]['audio'][gender]
        return {"encoded_audio": audio}

    def get_response(self, utterance: str, lang_code: str,
                     user_profile: UserProfile, node_data: NodeData):
        session = self.get_session(node_data)
        user_profile.user.username = (user_profile.user.username or
                                      self.mq_cliend_id)

        request_data = {"msg_type": "recognizer_loop:utterance",
                        "data": {"utterances": [utterance],
                                 "lang": lang_code},
                        "context": {"username": user_profile.user.username,
                                    "user_profiles": [
                                        user_profile.model_dump(mode="json")],
                                    "source": "hana",
                                    "session": session,
                                    "node_data": node_data.model_dump(
                                        mode="json"),
                                    "ident": f"{self.mq_cliend_id}{time()}"}}
        response = send_mq_request("/neon_chat_api", request_data,
                                   "neon_chat_api_request",
                                   timeout=self.mq_default_timeout)

        # Update session data for future inputs
        self.sessions_by_id[session['session_id']] = \
            response['context']['session']
        sentence = response['data']['responses'][lang_code]['sentence']
        return {"answer": sentence, "lang_code": lang_code}
