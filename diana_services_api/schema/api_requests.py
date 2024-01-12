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

from typing import Optional

from pydantic import BaseModel


class WeatherAPIRequest(BaseModel):
    api: str = "onecall"
    lat: float
    lon: float
    unit: str = "metric"

    model_config = {
        "json_schema_extra": {
            "examples": [{
                        "api": "onecall",
                        "lat": 47.6815,
                        "lon": -122.2087,
                        "unit": "imperial",
                    }, {
                        "api": "onecall",
                        "lat": 47.6815,
                        "lon": -122.2087,
                        "unit": "metric",
                    }]}}


class StockAPISymbolRequest(BaseModel):
    company: Optional[str] = None
    model_config = {
        "json_schema_extra": {
            "examples": [{"company": "microsoft"}]}}


class StockAPIQuoteRequest(BaseModel):
    symbol: Optional[str] = None
    model_config = {
        "json_schema_extra": {
            "examples": [{"symbol": "GOOG"}]}}


class GeoAPIRequest(BaseModel):
    address: str

    model_config = {
        "json_schema_extra": {
            "examples": [{
                        "address": "1100 Bellevue Way NE Bellevue, WA"
                    }]}}


class GeoAPIReverseRequest(BaseModel):
    lat: float
    lon: float
    model_config = {
        "json_schema_extra": {
            "examples": [{
                        "lat": 47.6815,
                        "lon": -122.2087,
                    }]}}


class WolframAlphaAPIRequest(BaseModel):
    api: str
    unit: str = "metric"
    lat: float
    lon: float
    query: str


class ParseScriptRequest(BaseModel):
    script: str


class GetCouponsRequest(BaseModel):
    pass


class SendEmailRequest(BaseModel):
    recipient: str
    subject: str
    body: str
    attachments: Optional[str] = None


class UploadMetricRequest(BaseModel):
    metric_name: str
    metric_data: str
