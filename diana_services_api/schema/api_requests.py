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
from time import time
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
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "api": "spoken",
                "lat": 47.6815,
                "lon": -122.2087,
                "query": "how far away is the moon"
            }, {
                "api": "short",
                "lat": 47.6815,
                "lon": -122.2087,
                "query": "how far away is London"
            }, {
                "api": "full",
                "lat": 47.6815,
                "lon": -122.2087,
                "query": "what is the derivative of sin(x)"
            }
            ]}}


class SendEmailRequest(BaseModel):
    recipient: str
    subject: str
    body: str
    attachments: Optional[dict] = None
    model_config = {
        "json_schema_extra": {
            "examples": [{
                        "recipient": "developers@neon.ai",
                        "subject": "API test",
                        "body": "This is a test.\nGenerated from OpenAPI.",
                        "attachments": {"test.txt": "VGhpcyBpcyBhIHRlc3QgZmlsZQo="}
                    }]}}


class UploadMetricRequest(BaseModel):
    metric_name: str
    timestamp: str
    metric_data: dict = dict()
    model_config = {
        "json_schema_extra": {
            "examples": [{
                        "metric_name": "REST API Test",
                        "timestamp": str(time()),
                        "metric_data": {"test": True, "flag": "demo"}}]}}


class ParseScriptRequest(BaseModel):
    script: str
    metadata: dict = dict()
    model_config = {
        "json_schema_extra": {
            "examples": [{
                        "script": """
Script: Parser Test Script
Author: Daniel McKnight
Description:
    Just an example description to go with
    an example script. This will go in meta

# Timeout goto line 18
Timeout: 10, 18
# Timeout exit
Timeout: 20

Synonym: "Test Script"
    "Tester Script"
    "Another Synonym"
Claps: 2 Two clap action
    3 3 clap action
Language: en-us, male

Variable: no_val
Variable: with_val = "Test Value"

# This is a comment line separating header from execution (kinda)
Neon speak: inlined speak
Neon speak:
    Block speech start
    ...
    Block speech end
@pre-exec
Execute: hello world
voice_input(no_val)
IF no_val == with_val:
    Goto: pre-exec
ELSE:
    Reconvey: pre-exec

If "word" IN "this phrase word is in":
    Neon speak: "phrase"

Reconvey: pre-exec, file_param
Name Reconvey: "Someone", "some text", "/path/to/file"

Case {with_val}:
    "Some value"
        Neon speak: first
    "some other value"
        Neon speak:
            second

Case(no_val):
    "no_val_1":
        Execute: what time is it

Python: 1*2  # TODO: syntax check

LOOP check START
Set: new_val = no_val  # This logs an error because it isn't declared
# TODO: The following should warn/error
dne = "test"
voice_input(new_val)
LOOP check END
Email: "Mail Title", "email body goes here. could be a variable name in most cases"
Run: script_name_here
Exit""", "metadata": {"test": True, "context": "demo"}}]}}
