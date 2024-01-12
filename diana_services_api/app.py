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

from fastapi import FastAPI
from typing import Union

from diana_services_api.schema.api_requests import *
from diana_services_api.schema.api_responses import *
from diana_services_api.mq_service_api import MQServiceManager


def create_app():
    mq_connector = MQServiceManager()
    app = FastAPI()

    @app.post("/proxy/weather")
    async def api_proxy_weather(query: WeatherAPIRequest) -> WeatherAPIOnecallResponse:
        return mq_connector.query_api_proxy("open_weather_map", dict(query))

    @app.post("/proxy/stock/symbol")
    async def api_proxy_stock_symbol(query: StockAPISymbolRequest) -> StockAPISearchResponse:
        return mq_connector.query_api_proxy("alpha_vantage",
                                            {**dict(query),
                                             **{"api": "symbol"}})

    @app.post("/proxy/stock/quote")
    async def api_proxy_stock_quote(query: StockAPIQuoteRequest) -> StockAPIQuoteResponse:
        return mq_connector.query_api_proxy("alpha_vantage",
                                            {**dict(query), **{"api": "quote"}})

    @app.post("/proxy/geolocation/geocode")
    async def api_proxy_geolocation(query: GeoAPIRequest) -> GeoAPIGeocodeResponse:
        return mq_connector.query_api_proxy("map_maker", dict(query))

    @app.post("/proxy/geolocation/reverse")
    async def api_proxy_geolocation(query: GeoAPIReverseRequest) -> GeoAPIReverseResponse:
        return mq_connector.query_api_proxy("map_maker", dict(query))
    return app
