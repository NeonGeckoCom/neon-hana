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
from typing import Optional, Dict, Any, List
from uuid import uuid4

from fastapi import HTTPException

from neon_mq_connector.utils.client_utils import send_mq_request


class APIError(HTTPException):
    """
    Exception class representing errors in getting responses from the MQ API
    """


class MQServiceManager:
    def __init__(self, config: dict):
        self.mq_default_timeout = config.get('mq_default_timeout', 10)
        self.mq_cliend_id = config.get('mq_client_id') or str(uuid4())

    def _validate_api_proxy_response(self, response: dict):
        if response['status_code'] == 200:
            try:
                resp = json.loads(response['content'])
                if isinstance(resp, dict):
                    return resp
                # Reverse Geocode API returns a list; reformat that to a dict
                if isinstance(resp, list):
                    return {**resp.pop(0),
                            **{"alternate_results": resp}}
            except json.JSONDecodeError:
                resp = response['content']
            # Wolfram Spoken API returns a string; reformat that to a dict
            if isinstance(resp, str):
                return {"answer": resp}
        code = response['status_code'] if response['status_code'] > 200 else 500
        raise APIError(status_code=code, detail=response['content'])

    def query_api_proxy(self, service_name: str, query_params: dict,
                        timeout: int = 10):
        query_params['service'] = service_name
        response = send_mq_request("/neon_api", query_params, "neon_api_input",
                                   "neon_api_output", timeout)
        return self._validate_api_proxy_response(response)

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

    def get_stt(self, b64_audio: str, lang: str, timeout: int = 20):
        request_data = {"msg_type": "neon.get_stt",
                                    "data": {"audio_data": b64_audio,
                                             "utterances": [""],  # TODO: Compat
                                             "lang": lang},
                                    "context": {"source": "hana"}}
        response = send_mq_request("/neon_chat_api", request_data,
                                   "neon_chat_api_request", timeout=timeout)
        return response

    def get_tts(self, string: str, lang: str, gender: str, timeout: int = 20):
        request_data = {"msg_type": "neon.get_tts",
                                    "data": {"text": string,
                                             "utterance": "",  # TODO: Compat
                                             "speaker": {"name": "Neon",
                                                         "gender": gender,
                                                         "lang": lang},
                                             "lang": lang},
                                    "context": {"source": "hana"}}
        response = send_mq_request("/neon_chat_api", request_data,
                                   "neon_chat_api_request", timeout=timeout)
        return response