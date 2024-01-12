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

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


class WeatherAPIOnecallResponse(BaseModel):
    lat: float
    lon: float
    timezone: str
    timezone_offset: int
    current: Dict[str, Any]
    minutely: List[dict]
    hourly: List[dict]
    daily: List[dict]

    model_config = {
        "extra": "allow",
        "json_schema_extra": {
            "examples": [
                {
                    "lat": 47.6815,
                    "lon": -122.2087,
                    "timezone": "America/Los_Angeles",
                    "timezone_offset": -28800,
                    "current": {
                        "dt": 1705080482,
                        "sunrise": 1705074869,
                        "sunset": 1705106347,
                        "temp": 18.36,
                        "feels_like": 9.05,
                        "pressure": 1022,
                        "humidity": 66,
                        "dew_point": 9.93,
                        "uvi": 0.18,
                        "clouds": 75,
                        "visibility": 10000,
                        "wind_speed": 7,
                        "wind_deg": 360,
                        "wind_gust": 14,
                        "weather": [
                            {
                                "id": 803,
                                "main": "Clouds",
                                "description": "broken clouds",
                                "icon": "04d"
                            }
                        ]
                    },
                    "minutely": [
                        {
                            "dt": 1705080540,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705080600,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705080660,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705080720,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705080780,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705080840,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705080900,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705080960,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705081020,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705081080,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705081140,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705081200,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705081260,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705081320,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705081380,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705081440,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705081500,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705081560,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705081620,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705081680,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705081740,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705081800,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705081860,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705081920,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705081980,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705082040,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705082100,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705082160,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705082220,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705082280,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705082340,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705082400,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705082460,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705082520,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705082580,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705082640,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705082700,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705082760,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705082820,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705082880,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705082940,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705083000,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705083060,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705083120,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705083180,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705083240,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705083300,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705083360,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705083420,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705083480,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705083540,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705083600,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705083660,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705083720,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705083780,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705083840,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705083900,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705083960,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705084020,
                            "precipitation": 0
                        },
                        {
                            "dt": 1705084080,
                            "precipitation": 0
                        }
                    ],
                    "hourly": [
                        {
                            "dt": 1705078800,
                            "temp": 18.36,
                            "feels_like": 8.4,
                            "pressure": 1022,
                            "humidity": 66,
                            "dew_point": 9.93,
                            "uvi": 0.18,
                            "clouds": 75,
                            "visibility": 10000,
                            "wind_speed": 7.78,
                            "wind_deg": 345,
                            "wind_gust": 11.9,
                            "weather": [
                                {
                                    "id": 803,
                                    "main": "Clouds",
                                    "description": "broken clouds",
                                    "icon": "04d"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705082400,
                            "temp": 18.37,
                            "feels_like": 8.19,
                            "pressure": 1022,
                            "humidity": 63,
                            "dew_point": 9.01,
                            "uvi": 0.41,
                            "clouds": 72,
                            "visibility": 10000,
                            "wind_speed": 8.08,
                            "wind_deg": 346,
                            "wind_gust": 10.65,
                            "weather": [
                                {
                                    "id": 803,
                                    "main": "Clouds",
                                    "description": "broken clouds",
                                    "icon": "04d"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705086000,
                            "temp": 18.91,
                            "feels_like": 9.01,
                            "pressure": 1023,
                            "humidity": 60,
                            "dew_point": 8.56,
                            "uvi": 0.66,
                            "clouds": 49,
                            "visibility": 10000,
                            "wind_speed": 7.87,
                            "wind_deg": 348,
                            "wind_gust": 9.31,
                            "weather": [
                                {
                                    "id": 802,
                                    "main": "Clouds",
                                    "description": "scattered clouds",
                                    "icon": "03d"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705089600,
                            "temp": 19.74,
                            "feels_like": 9.99,
                            "pressure": 1024,
                            "humidity": 55,
                            "dew_point": 7.65,
                            "uvi": 0.78,
                            "clouds": 35,
                            "visibility": 10000,
                            "wind_speed": 7.92,
                            "wind_deg": 348,
                            "wind_gust": 8.97,
                            "weather": [
                                {
                                    "id": 802,
                                    "main": "Clouds",
                                    "description": "scattered clouds",
                                    "icon": "03d"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705093200,
                            "temp": 20.77,
                            "feels_like": 11.23,
                            "pressure": 1024,
                            "humidity": 50,
                            "dew_point": 6.73,
                            "uvi": 0.72,
                            "clouds": 21,
                            "visibility": 10000,
                            "wind_speed": 7.92,
                            "wind_deg": 350,
                            "wind_gust": 8.52,
                            "weather": [
                                {
                                    "id": 801,
                                    "main": "Clouds",
                                    "description": "few clouds",
                                    "icon": "02d"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705096800,
                            "temp": 21.67,
                            "feels_like": 12.24,
                            "pressure": 1024,
                            "humidity": 47,
                            "dew_point": 3.74,
                            "uvi": 0.52,
                            "clouds": 7,
                            "visibility": 10000,
                            "wind_speed": 8.03,
                            "wind_deg": 353,
                            "wind_gust": 8.97,
                            "weather": [
                                {
                                    "id": 800,
                                    "main": "Clear",
                                    "description": "clear sky",
                                    "icon": "01d"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705100400,
                            "temp": 21.54,
                            "feels_like": 12.09,
                            "pressure": 1024,
                            "humidity": 48,
                            "dew_point": 3.83,
                            "uvi": 0.26,
                            "clouds": 9,
                            "visibility": 10000,
                            "wind_speed": 8.03,
                            "wind_deg": 352,
                            "wind_gust": 9.19,
                            "weather": [
                                {
                                    "id": 800,
                                    "main": "Clear",
                                    "description": "clear sky",
                                    "icon": "01d"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705104000,
                            "temp": 20.66,
                            "feels_like": 11.16,
                            "pressure": 1024,
                            "humidity": 51,
                            "dew_point": 4.28,
                            "uvi": 0,
                            "clouds": 13,
                            "visibility": 10000,
                            "wind_speed": 7.85,
                            "wind_deg": 350,
                            "wind_gust": 10.54,
                            "weather": [
                                {
                                    "id": 801,
                                    "main": "Clouds",
                                    "description": "few clouds",
                                    "icon": "02d"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705107600,
                            "temp": 19.15,
                            "feels_like": 10.02,
                            "pressure": 1024,
                            "humidity": 54,
                            "dew_point": 4.1,
                            "uvi": 0,
                            "clouds": 27,
                            "visibility": 10000,
                            "wind_speed": 6.98,
                            "wind_deg": 351,
                            "wind_gust": 12.08,
                            "weather": [
                                {
                                    "id": 802,
                                    "main": "Clouds",
                                    "description": "scattered clouds",
                                    "icon": "03n"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705111200,
                            "temp": 18.68,
                            "feels_like": 10.29,
                            "pressure": 1024,
                            "humidity": 55,
                            "dew_point": 4.19,
                            "uvi": 0,
                            "clouds": 33,
                            "visibility": 10000,
                            "wind_speed": 6.08,
                            "wind_deg": 4,
                            "wind_gust": 13.02,
                            "weather": [
                                {
                                    "id": 802,
                                    "main": "Clouds",
                                    "description": "scattered clouds",
                                    "icon": "03n"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705114800,
                            "temp": 18.39,
                            "feels_like": 11.01,
                            "pressure": 1024,
                            "humidity": 56,
                            "dew_point": 4.15,
                            "uvi": 0,
                            "clouds": 36,
                            "visibility": 10000,
                            "wind_speed": 5.08,
                            "wind_deg": 21,
                            "wind_gust": 11.43,
                            "weather": [
                                {
                                    "id": 802,
                                    "main": "Clouds",
                                    "description": "scattered clouds",
                                    "icon": "03n"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705118400,
                            "temp": 17.67,
                            "feels_like": 9.88,
                            "pressure": 1024,
                            "humidity": 57,
                            "dew_point": 3.92,
                            "uvi": 0,
                            "clouds": 46,
                            "visibility": 10000,
                            "wind_speed": 5.32,
                            "wind_deg": 52,
                            "wind_gust": 10.56,
                            "weather": [
                                {
                                    "id": 802,
                                    "main": "Clouds",
                                    "description": "scattered clouds",
                                    "icon": "03n"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705122000,
                            "temp": 16.07,
                            "feels_like": 7.65,
                            "pressure": 1024,
                            "humidity": 57,
                            "dew_point": 2.17,
                            "uvi": 0,
                            "clouds": 56,
                            "visibility": 10000,
                            "wind_speed": 5.64,
                            "wind_deg": 72,
                            "wind_gust": 8.61,
                            "weather": [
                                {
                                    "id": 803,
                                    "main": "Clouds",
                                    "description": "broken clouds",
                                    "icon": "04n"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705125600,
                            "temp": 14.31,
                            "feels_like": 4.93,
                            "pressure": 1024,
                            "humidity": 54,
                            "dew_point": -0.89,
                            "uvi": 0,
                            "clouds": 64,
                            "visibility": 10000,
                            "wind_speed": 6.22,
                            "wind_deg": 85,
                            "wind_gust": 9.31,
                            "weather": [
                                {
                                    "id": 803,
                                    "main": "Clouds",
                                    "description": "broken clouds",
                                    "icon": "04n"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705129200,
                            "temp": 13.59,
                            "feels_like": 4.37,
                            "pressure": 1024,
                            "humidity": 49,
                            "dew_point": -3.46,
                            "uvi": 0,
                            "clouds": 99,
                            "visibility": 10000,
                            "wind_speed": 5.93,
                            "wind_deg": 83,
                            "wind_gust": 9.01,
                            "weather": [
                                {
                                    "id": 804,
                                    "main": "Clouds",
                                    "description": "overcast clouds",
                                    "icon": "04n"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705132800,
                            "temp": 13.01,
                            "feels_like": 3.31,
                            "pressure": 1023,
                            "humidity": 46,
                            "dew_point": -5.46,
                            "uvi": 0,
                            "clouds": 100,
                            "visibility": 10000,
                            "wind_speed": 6.29,
                            "wind_deg": 83,
                            "wind_gust": 9.71,
                            "weather": [
                                {
                                    "id": 804,
                                    "main": "Clouds",
                                    "description": "overcast clouds",
                                    "icon": "04n"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705136400,
                            "temp": 12.36,
                            "feels_like": 2.5,
                            "pressure": 1023,
                            "humidity": 45,
                            "dew_point": -6.5,
                            "uvi": 0,
                            "clouds": 100,
                            "visibility": 10000,
                            "wind_speed": 6.33,
                            "wind_deg": 77,
                            "wind_gust": 9.84,
                            "weather": [
                                {
                                    "id": 804,
                                    "main": "Clouds",
                                    "description": "overcast clouds",
                                    "icon": "04n"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705140000,
                            "temp": 11.8,
                            "feels_like": 2.59,
                            "pressure": 1022,
                            "humidity": 45,
                            "dew_point": -7.19,
                            "uvi": 0,
                            "clouds": 100,
                            "visibility": 10000,
                            "wind_speed": 5.64,
                            "wind_deg": 75,
                            "wind_gust": 8.79,
                            "weather": [
                                {
                                    "id": 804,
                                    "main": "Clouds",
                                    "description": "overcast clouds",
                                    "icon": "04n"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705143600,
                            "temp": 11.39,
                            "feels_like": 1.42,
                            "pressure": 1022,
                            "humidity": 45,
                            "dew_point": -7.78,
                            "uvi": 0,
                            "clouds": 100,
                            "visibility": 10000,
                            "wind_speed": 6.24,
                            "wind_deg": 75,
                            "wind_gust": 9.78,
                            "weather": [
                                {
                                    "id": 804,
                                    "main": "Clouds",
                                    "description": "overcast clouds",
                                    "icon": "04n"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705147200,
                            "temp": 10.71,
                            "feels_like": 0.73,
                            "pressure": 1021,
                            "humidity": 45,
                            "dew_point": -8.55,
                            "uvi": 0,
                            "clouds": 100,
                            "visibility": 10000,
                            "wind_speed": 6.13,
                            "wind_deg": 77,
                            "wind_gust": 9.84,
                            "weather": [
                                {
                                    "id": 804,
                                    "main": "Clouds",
                                    "description": "overcast clouds",
                                    "icon": "04n"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705150800,
                            "temp": 10.4,
                            "feels_like": -0.04,
                            "pressure": 1020,
                            "humidity": 44,
                            "dew_point": -9.15,
                            "uvi": 0,
                            "clouds": 100,
                            "visibility": 10000,
                            "wind_speed": 6.51,
                            "wind_deg": 77,
                            "wind_gust": 10.33,
                            "weather": [
                                {
                                    "id": 804,
                                    "main": "Clouds",
                                    "description": "overcast clouds",
                                    "icon": "04n"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705154400,
                            "temp": 9.97,
                            "feels_like": -0.2,
                            "pressure": 1019,
                            "humidity": 44,
                            "dew_point": -9.89,
                            "uvi": 0,
                            "clouds": 100,
                            "visibility": 10000,
                            "wind_speed": 6.17,
                            "wind_deg": 73,
                            "wind_gust": 10,
                            "weather": [
                                {
                                    "id": 804,
                                    "main": "Clouds",
                                    "description": "overcast clouds",
                                    "icon": "04n"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705158000,
                            "temp": 9.88,
                            "feels_like": 0.64,
                            "pressure": 1019,
                            "humidity": 43,
                            "dew_point": -10.3,
                            "uvi": 0,
                            "clouds": 100,
                            "visibility": 10000,
                            "wind_speed": 5.35,
                            "wind_deg": 69,
                            "wind_gust": 8.28,
                            "weather": [
                                {
                                    "id": 804,
                                    "main": "Clouds",
                                    "description": "overcast clouds",
                                    "icon": "04n"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705161600,
                            "temp": 9.39,
                            "feels_like": 0.1,
                            "pressure": 1018,
                            "humidity": 44,
                            "dew_point": -10.37,
                            "uvi": 0,
                            "clouds": 100,
                            "visibility": 10000,
                            "wind_speed": 5.32,
                            "wind_deg": 70,
                            "wind_gust": 8.9,
                            "weather": [
                                {
                                    "id": 804,
                                    "main": "Clouds",
                                    "description": "overcast clouds",
                                    "icon": "04d"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705165200,
                            "temp": 10.35,
                            "feels_like": 1.8,
                            "pressure": 1017,
                            "humidity": 43,
                            "dew_point": -9.99,
                            "uvi": 0.16,
                            "clouds": 100,
                            "visibility": 10000,
                            "wind_speed": 4.88,
                            "wind_deg": 72,
                            "wind_gust": 8.32,
                            "weather": [
                                {
                                    "id": 804,
                                    "main": "Clouds",
                                    "description": "overcast clouds",
                                    "icon": "04d"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705168800,
                            "temp": 12.11,
                            "feels_like": 1.4,
                            "pressure": 1016,
                            "humidity": 40,
                            "dew_point": -9.29,
                            "uvi": 0.36,
                            "clouds": 100,
                            "visibility": 10000,
                            "wind_speed": 7.14,
                            "wind_deg": 61,
                            "wind_gust": 11.32,
                            "weather": [
                                {
                                    "id": 804,
                                    "main": "Clouds",
                                    "description": "overcast clouds",
                                    "icon": "04d"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705172400,
                            "temp": 14.52,
                            "feels_like": 5.34,
                            "pressure": 1014,
                            "humidity": 38,
                            "dew_point": -8.27,
                            "uvi": 0.5,
                            "clouds": 100,
                            "visibility": 10000,
                            "wind_speed": 6.06,
                            "wind_deg": 59,
                            "wind_gust": 10.13,
                            "weather": [
                                {
                                    "id": 804,
                                    "main": "Clouds",
                                    "description": "overcast clouds",
                                    "icon": "04d"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705176000,
                            "temp": 17.11,
                            "feels_like": 9.99,
                            "pressure": 1014,
                            "humidity": 36,
                            "dew_point": -6.72,
                            "uvi": 0.62,
                            "clouds": 100,
                            "visibility": 10000,
                            "wind_speed": 4.68,
                            "wind_deg": 54,
                            "wind_gust": 7.96,
                            "weather": [
                                {
                                    "id": 804,
                                    "main": "Clouds",
                                    "description": "overcast clouds",
                                    "icon": "04d"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705179600,
                            "temp": 18.7,
                            "feels_like": 10.42,
                            "pressure": 1012,
                            "humidity": 36,
                            "dew_point": -5.01,
                            "uvi": 0.58,
                            "clouds": 100,
                            "visibility": 10000,
                            "wind_speed": 5.97,
                            "wind_deg": 53,
                            "wind_gust": 9.91,
                            "weather": [
                                {
                                    "id": 804,
                                    "main": "Clouds",
                                    "description": "overcast clouds",
                                    "icon": "04d"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705183200,
                            "temp": 19.42,
                            "feels_like": 11.01,
                            "pressure": 1011,
                            "humidity": 37,
                            "dew_point": -3.53,
                            "uvi": 0.47,
                            "clouds": 100,
                            "visibility": 10000,
                            "wind_speed": 6.24,
                            "wind_deg": 51,
                            "wind_gust": 9.86,
                            "weather": [
                                {
                                    "id": 804,
                                    "main": "Clouds",
                                    "description": "overcast clouds",
                                    "icon": "04d"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705186800,
                            "temp": 19.15,
                            "feels_like": 10.17,
                            "pressure": 1010,
                            "humidity": 40,
                            "dew_point": -2.43,
                            "uvi": 0.25,
                            "clouds": 100,
                            "visibility": 10000,
                            "wind_speed": 6.82,
                            "wind_deg": 45,
                            "wind_gust": 11.01,
                            "weather": [
                                {
                                    "id": 804,
                                    "main": "Clouds",
                                    "description": "overcast clouds",
                                    "icon": "04d"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705190400,
                            "temp": 18.07,
                            "feels_like": 9.61,
                            "pressure": 1010,
                            "humidity": 43,
                            "dew_point": -1.57,
                            "uvi": 0,
                            "clouds": 100,
                            "visibility": 10000,
                            "wind_speed": 6.04,
                            "wind_deg": 50,
                            "wind_gust": 10.87,
                            "weather": [
                                {
                                    "id": 804,
                                    "main": "Clouds",
                                    "description": "overcast clouds",
                                    "icon": "04d"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705194000,
                            "temp": 16.54,
                            "feels_like": 8.38,
                            "pressure": 1011,
                            "humidity": 48,
                            "dew_point": -0.98,
                            "uvi": 0,
                            "clouds": 100,
                            "visibility": 10000,
                            "wind_speed": 5.46,
                            "wind_deg": 57,
                            "wind_gust": 9.82,
                            "weather": [
                                {
                                    "id": 804,
                                    "main": "Clouds",
                                    "description": "overcast clouds",
                                    "icon": "04n"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705197600,
                            "temp": 15.53,
                            "feels_like": 7.2,
                            "pressure": 1011,
                            "humidity": 49,
                            "dew_point": -1.44,
                            "uvi": 0,
                            "clouds": 100,
                            "visibility": 10000,
                            "wind_speed": 5.46,
                            "wind_deg": 62,
                            "wind_gust": 10.71,
                            "weather": [
                                {
                                    "id": 804,
                                    "main": "Clouds",
                                    "description": "overcast clouds",
                                    "icon": "04n"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705201200,
                            "temp": 14.92,
                            "feels_like": 6.87,
                            "pressure": 1012,
                            "humidity": 48,
                            "dew_point": -2.6,
                            "uvi": 0,
                            "clouds": 100,
                            "visibility": 10000,
                            "wind_speed": 5.12,
                            "wind_deg": 76,
                            "wind_gust": 9.4,
                            "weather": [
                                {
                                    "id": 804,
                                    "main": "Clouds",
                                    "description": "overcast clouds",
                                    "icon": "04n"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705204800,
                            "temp": 14.5,
                            "feels_like": 6.87,
                            "pressure": 1013,
                            "humidity": 48,
                            "dew_point": -2.85,
                            "uvi": 0,
                            "clouds": 100,
                            "visibility": 10000,
                            "wind_speed": 4.72,
                            "wind_deg": 91,
                            "wind_gust": 8.97,
                            "weather": [
                                {
                                    "id": 804,
                                    "main": "Clouds",
                                    "description": "overcast clouds",
                                    "icon": "04n"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705208400,
                            "temp": 14.47,
                            "feels_like": 6.42,
                            "pressure": 1014,
                            "humidity": 48,
                            "dew_point": -2.92,
                            "uvi": 0,
                            "clouds": 100,
                            "visibility": 10000,
                            "wind_speed": 5.06,
                            "wind_deg": 94,
                            "wind_gust": 9.13,
                            "weather": [
                                {
                                    "id": 804,
                                    "main": "Clouds",
                                    "description": "overcast clouds",
                                    "icon": "04n"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705212000,
                            "temp": 14.56,
                            "feels_like": 7.95,
                            "pressure": 1014,
                            "humidity": 47,
                            "dew_point": -3.28,
                            "uvi": 0,
                            "clouds": 100,
                            "visibility": 10000,
                            "wind_speed": 3.98,
                            "wind_deg": 82,
                            "wind_gust": 7.27,
                            "weather": [
                                {
                                    "id": 804,
                                    "main": "Clouds",
                                    "description": "overcast clouds",
                                    "icon": "04n"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705215600,
                            "temp": 14.86,
                            "feels_like": 8.28,
                            "pressure": 1015,
                            "humidity": 46,
                            "dew_point": -3.77,
                            "uvi": 0,
                            "clouds": 100,
                            "visibility": 10000,
                            "wind_speed": 4,
                            "wind_deg": 82,
                            "wind_gust": 7.18,
                            "weather": [
                                {
                                    "id": 804,
                                    "main": "Clouds",
                                    "description": "overcast clouds",
                                    "icon": "04n"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705219200,
                            "temp": 15.08,
                            "feels_like": 9.28,
                            "pressure": 1015,
                            "humidity": 45,
                            "dew_point": -3.69,
                            "uvi": 0,
                            "clouds": 100,
                            "visibility": 10000,
                            "wind_speed": 3.51,
                            "wind_deg": 90,
                            "wind_gust": 6.53,
                            "weather": [
                                {
                                    "id": 804,
                                    "main": "Clouds",
                                    "description": "overcast clouds",
                                    "icon": "04n"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705222800,
                            "temp": 15.01,
                            "feels_like": 15.01,
                            "pressure": 1016,
                            "humidity": 47,
                            "dew_point": -3.01,
                            "uvi": 0,
                            "clouds": 100,
                            "visibility": 10000,
                            "wind_speed": 2.48,
                            "wind_deg": 82,
                            "wind_gust": 4.59,
                            "weather": [
                                {
                                    "id": 804,
                                    "main": "Clouds",
                                    "description": "overcast clouds",
                                    "icon": "04n"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705226400,
                            "temp": 15.22,
                            "feels_like": 9.55,
                            "pressure": 1017,
                            "humidity": 48,
                            "dew_point": -2.34,
                            "uvi": 0,
                            "clouds": 100,
                            "visibility": 10000,
                            "wind_speed": 3.44,
                            "wind_deg": 103,
                            "wind_gust": 6.24,
                            "weather": [
                                {
                                    "id": 804,
                                    "main": "Clouds",
                                    "description": "overcast clouds",
                                    "icon": "04n"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705230000,
                            "temp": 15.21,
                            "feels_like": 15.21,
                            "pressure": 1018,
                            "humidity": 50,
                            "dew_point": -1.41,
                            "uvi": 0,
                            "clouds": 99,
                            "visibility": 10000,
                            "wind_speed": 1.7,
                            "wind_deg": 101,
                            "wind_gust": 2.93,
                            "weather": [
                                {
                                    "id": 804,
                                    "main": "Clouds",
                                    "description": "overcast clouds",
                                    "icon": "04n"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705233600,
                            "temp": 15.19,
                            "feels_like": 15.19,
                            "pressure": 1019,
                            "humidity": 52,
                            "dew_point": -0.51,
                            "uvi": 0,
                            "clouds": 89,
                            "visibility": 10000,
                            "wind_speed": 2.98,
                            "wind_deg": 105,
                            "wind_gust": 4.88,
                            "weather": [
                                {
                                    "id": 804,
                                    "main": "Clouds",
                                    "description": "overcast clouds",
                                    "icon": "04n"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705237200,
                            "temp": 15.71,
                            "feels_like": 15.71,
                            "pressure": 1019,
                            "humidity": 53,
                            "dew_point": 0.32,
                            "uvi": 0,
                            "clouds": 96,
                            "visibility": 10000,
                            "wind_speed": 2.13,
                            "wind_deg": 118,
                            "wind_gust": 4.07,
                            "weather": [
                                {
                                    "id": 804,
                                    "main": "Clouds",
                                    "description": "overcast clouds",
                                    "icon": "04n"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705240800,
                            "temp": 15.26,
                            "feels_like": 10.09,
                            "pressure": 1020,
                            "humidity": 56,
                            "dew_point": 1.04,
                            "uvi": 0,
                            "clouds": 56,
                            "visibility": 10000,
                            "wind_speed": 3.15,
                            "wind_deg": 130,
                            "wind_gust": 5.44,
                            "weather": [
                                {
                                    "id": 803,
                                    "main": "Clouds",
                                    "description": "broken clouds",
                                    "icon": "04n"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705244400,
                            "temp": 15.26,
                            "feels_like": 15.26,
                            "pressure": 1021,
                            "humidity": 57,
                            "dew_point": 1.53,
                            "uvi": 0,
                            "clouds": 40,
                            "visibility": 10000,
                            "wind_speed": 2.68,
                            "wind_deg": 122,
                            "wind_gust": 4.05,
                            "weather": [
                                {
                                    "id": 802,
                                    "main": "Clouds",
                                    "description": "scattered clouds",
                                    "icon": "03n"
                                }
                            ],
                            "pop": 0
                        },
                        {
                            "dt": 1705248000,
                            "temp": 15.31,
                            "feels_like": 15.31,
                            "pressure": 1022,
                            "humidity": 58,
                            "dew_point": 1.83,
                            "uvi": 0,
                            "clouds": 32,
                            "visibility": 10000,
                            "wind_speed": 2.93,
                            "wind_deg": 129,
                            "wind_gust": 4.32,
                            "weather": [
                                {
                                    "id": 802,
                                    "main": "Clouds",
                                    "description": "scattered clouds",
                                    "icon": "03d"
                                }
                            ],
                            "pop": 0
                        }
                    ],
                    "daily": [
                        {
                            "dt": 1705089600,
                            "sunrise": 1705074869,
                            "sunset": 1705106347,
                            "moonrise": 1705080180,
                            "moonset": 1705111980,
                            "moon_phase": 0.05,
                            "temp": {
                                "day": 19.74,
                                "min": 13.59,
                                "max": 25.88,
                                "night": 13.59,
                                "eve": 18.68,
                                "morn": 18.7
                            },
                            "feels_like": {
                                "day": 9.99,
                                "night": 4.37,
                                "eve": 10.29,
                                "morn": 8.56
                            },
                            "pressure": 1024,
                            "humidity": 55,
                            "dew_point": 7.65,
                            "wind_speed": 9.62,
                            "wind_deg": 328,
                            "wind_gust": 17.87,
                            "weather": [
                                {
                                    "id": 802,
                                    "main": "Clouds",
                                    "description": "scattered clouds",
                                    "icon": "03d"
                                }
                            ],
                            "clouds": 35,
                            "pop": 0.43,
                            "uvi": 0.78
                        },
                        {
                            "dt": 1705176000,
                            "sunrise": 1705161237,
                            "sunset": 1705192824,
                            "moonrise": 1705168260,
                            "moonset": 1705203660,
                            "moon_phase": 0.09,
                            "temp": {
                                "day": 17.11,
                                "min": 9.39,
                                "max": 19.42,
                                "night": 14.86,
                                "eve": 15.53,
                                "morn": 9.97
                            },
                            "feels_like": {
                                "day": 9.99,
                                "night": 8.28,
                                "eve": 7.2,
                                "morn": -0.2
                            },
                            "pressure": 1014,
                            "humidity": 36,
                            "dew_point": -6.72,
                            "wind_speed": 7.14,
                            "wind_deg": 61,
                            "wind_gust": 11.32,
                            "weather": [
                                {
                                    "id": 804,
                                    "main": "Clouds",
                                    "description": "overcast clouds",
                                    "icon": "04d"
                                }
                            ],
                            "clouds": 100,
                            "pop": 0,
                            "uvi": 0.62
                        },
                        {
                            "dt": 1705262400,
                            "sunrise": 1705247602,
                            "sunset": 1705279304,
                            "moonrise": 1705255920,
                            "moonset": 1705295220,
                            "moon_phase": 0.13,
                            "temp": {
                                "day": 26.42,
                                "min": 15.01,
                                "max": 27.97,
                                "night": 22.41,
                                "eve": 23.58,
                                "morn": 15.26
                            },
                            "feels_like": {
                                "day": 26.42,
                                "night": 22.41,
                                "eve": 23.58,
                                "morn": 10.09
                            },
                            "pressure": 1023,
                            "humidity": 40,
                            "dew_point": 4.87,
                            "wind_speed": 3.51,
                            "wind_deg": 90,
                            "wind_gust": 6.53,
                            "weather": [
                                {
                                    "id": 803,
                                    "main": "Clouds",
                                    "description": "broken clouds",
                                    "icon": "04d"
                                }
                            ],
                            "clouds": 65,
                            "pop": 0,
                            "uvi": 0.73
                        },
                        {
                            "dt": 1705348800,
                            "sunrise": 1705333965,
                            "sunset": 1705365784,
                            "moonrise": 1705343460,
                            "moonset": 1705386480,
                            "moon_phase": 0.16,
                            "temp": {
                                "day": 32.43,
                                "min": 20.66,
                                "max": 32.43,
                                "night": 24.03,
                                "eve": 25.74,
                                "morn": 20.66
                            },
                            "feels_like": {
                                "day": 32.43,
                                "night": 20.05,
                                "eve": 21.63,
                                "morn": 20.66
                            },
                            "pressure": 1029,
                            "humidity": 41,
                            "dew_point": 11.03,
                            "wind_speed": 3.4,
                            "wind_deg": 80,
                            "wind_gust": 6.11,
                            "weather": [
                                {
                                    "id": 804,
                                    "main": "Clouds",
                                    "description": "overcast clouds",
                                    "icon": "04d"
                                }
                            ],
                            "clouds": 98,
                            "pop": 0,
                            "uvi": 0.9
                        },
                        {
                            "dt": 1705435200,
                            "sunrise": 1705420325,
                            "sunset": 1705452267,
                            "moonrise": 1705430880,
                            "moonset": 1705477740,
                            "moon_phase": 0.2,
                            "temp": {
                                "day": 35.67,
                                "min": 23.2,
                                "max": 35.67,
                                "night": 31.51,
                                "eve": 29.66,
                                "morn": 23.4
                            },
                            "feels_like": {
                                "day": 35.67,
                                "night": 28.67,
                                "eve": 26.51,
                                "morn": 23.4
                            },
                            "pressure": 1026,
                            "humidity": 42,
                            "dew_point": 14.59,
                            "wind_speed": 3.11,
                            "wind_deg": 132,
                            "wind_gust": 5.21,
                            "weather": [
                                {
                                    "id": 804,
                                    "main": "Clouds",
                                    "description": "overcast clouds",
                                    "icon": "04d"
                                }
                            ],
                            "clouds": 97,
                            "pop": 0,
                            "uvi": 1
                        },
                        {
                            "dt": 1705521600,
                            "sunrise": 1705506683,
                            "sunset": 1705538750,
                            "moonrise": 1705518360,
                            "moonset": 0,
                            "moon_phase": 0.25,
                            "temp": {
                                "day": 36.27,
                                "min": 33.31,
                                "max": 36.27,
                                "night": 36.23,
                                "eve": 36,
                                "morn": 33.44
                            },
                            "feels_like": {
                                "day": 36.27,
                                "night": 36.23,
                                "eve": 36,
                                "morn": 33.44
                            },
                            "pressure": 1024,
                            "humidity": 95,
                            "dew_point": 34.72,
                            "wind_speed": 2.42,
                            "wind_deg": 155,
                            "wind_gust": 2.62,
                            "weather": [
                                {
                                    "id": 500,
                                    "main": "Rain",
                                    "description": "light rain",
                                    "icon": "10d"
                                }
                            ],
                            "clouds": 100,
                            "pop": 0.9,
                            "rain": 2.34,
                            "uvi": 1
                        },
                        {
                            "dt": 1705608000,
                            "sunrise": 1705593038,
                            "sunset": 1705625235,
                            "moonrise": 1705605900,
                            "moonset": 1705568880,
                            "moon_phase": 0.27,
                            "temp": {
                                "day": 39.09,
                                "min": 36.5,
                                "max": 40.23,
                                "night": 40.23,
                                "eve": 39.79,
                                "morn": 37.13
                            },
                            "feels_like": {
                                "day": 39.09,
                                "night": 40.23,
                                "eve": 39.79,
                                "morn": 37.13
                            },
                            "pressure": 1024,
                            "humidity": 98,
                            "dew_point": 38.34,
                            "wind_speed": 3.22,
                            "wind_deg": 29,
                            "wind_gust": 3.04,
                            "weather": [
                                {
                                    "id": 500,
                                    "main": "Rain",
                                    "description": "light rain",
                                    "icon": "10d"
                                }
                            ],
                            "clouds": 100,
                            "pop": 0.88,
                            "rain": 3.3,
                            "uvi": 1
                        },
                        {
                            "dt": 1705694400,
                            "sunrise": 1705679391,
                            "sunset": 1705711720,
                            "moonrise": 1705693620,
                            "moonset": 1705659960,
                            "moon_phase": 0.31,
                            "temp": {
                                "day": 50.5,
                                "min": 39.88,
                                "max": 50.5,
                                "night": 40.96,
                                "eve": 44.17,
                                "morn": 39.88
                            },
                            "feels_like": {
                                "day": 49.39,
                                "night": 38.59,
                                "eve": 44.17,
                                "morn": 38.16
                            },
                            "pressure": 1022,
                            "humidity": 88,
                            "dew_point": 46.85,
                            "wind_speed": 3.83,
                            "wind_deg": 129,
                            "wind_gust": 4.29,
                            "weather": [
                                {
                                    "id": 803,
                                    "main": "Clouds",
                                    "description": "broken clouds",
                                    "icon": "04d"
                                }
                            ],
                            "clouds": 63,
                            "pop": 0,
                            "uvi": 1
                        }
                    ]
                }
            ]
        }
    }


class StockAPIQuoteResponse(BaseModel):
    global_quote: Dict[str, str] = Field(..., alias="Global Quote")

    model_config = {
        "extra": "allow",
        "json_schema_extra": {
            "examples": [
                {
                    "Global Quote": {
                        "01. symbol": "GOOG",
                        "02. open": "144.8950",
                        "03. high": "146.6600",
                        "04. low": "142.2150",
                        "05. price": "143.6700",
                        "06. volume": "17471130",
                        "07. latest trading day": "2024-01-11",
                        "08. previous close": "143.8000",
                        "09. change": "-0.1300",
                        "10. change percent": "-0.0904%"
                    }
                }
            ]}}


class StockAPISearchResponse(BaseModel):
    model_config = {
        "extra": "allow",
        "json_schema_extra": {
            "examples": [
                {
                    "bestMatches": [
                        {
                            "1. symbol": "MSF0.FRK",
                            "2. name": "MICROSOFT CORP. CDR",
                            "3. type": "Equity",
                            "4. region": "Frankfurt",
                            "5. marketOpen": "08:00",
                            "6. marketClose": "20:00",
                            "7. timezone": "UTC+02",
                            "8. currency": "EUR",
                            "9. matchScore": "0.6429"
                        },
                        {
                            "1. symbol": "MSFT",
                            "2. name": "Microsoft Corporation",
                            "3. type": "Equity",
                            "4. region": "United States",
                            "5. marketOpen": "09:30",
                            "6. marketClose": "16:00",
                            "7. timezone": "UTC-04",
                            "8. currency": "USD",
                            "9. matchScore": "0.6154"
                        },
                        {
                            "1. symbol": "0QYP.LON",
                            "2. name": "Microsoft Corporation",
                            "3. type": "Equity",
                            "4. region": "United Kingdom",
                            "5. marketOpen": "08:00",
                            "6. marketClose": "16:30",
                            "7. timezone": "UTC+01",
                            "8. currency": "USD",
                            "9. matchScore": "0.6000"
                        },
                        {
                            "1. symbol": "MSF.DEX",
                            "2. name": "Microsoft Corporation",
                            "3. type": "Equity",
                            "4. region": "XETRA",
                            "5. marketOpen": "08:00",
                            "6. marketClose": "20:00",
                            "7. timezone": "UTC+02",
                            "8. currency": "EUR",
                            "9. matchScore": "0.6000"
                        },
                        {
                            "1. symbol": "MSF.FRK",
                            "2. name": "Microsoft Corporation",
                            "3. type": "Equity",
                            "4. region": "Frankfurt",
                            "5. marketOpen": "08:00",
                            "6. marketClose": "20:00",
                            "7. timezone": "UTC+02",
                            "8. currency": "EUR",
                            "9. matchScore": "0.6000"
                        },
                        {
                            "1. symbol": "MSFT34.SAO",
                            "2. name": "Microsoft Corporation",
                            "3. type": "Equity",
                            "4. region": "Brazil/Sao Paolo",
                            "5. marketOpen": "10:00",
                            "6. marketClose": "17:30",
                            "7. timezone": "UTC-03",
                            "8. currency": "BRL",
                            "9. matchScore": "0.6000"
                        }
                    ]
                }]}}


class GeoAPIGeocodeResponse(BaseModel):
    place_id: int
    licence: str
    osm_type: str
    osm_id: int
    boundingbox: List[str]
    lat: str
    lon: str
    display_name: str
    class_: Optional[str] = Field(..., alias="class")
    type_: Optional[str] = Field(..., alias="type")
    importance: float
    alternate_results: List[dict]

    model_config = {
        "extra": "allow",
        "json_schema_extra": {
            "examples": [
                {
                    "place_id": 288749081,
                    "licence": "Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright",
                    "osm_type": "node",
                    "osm_id": 9106438617,
                    "boundingbox": [
                        "47.6204274",
                        "47.6205274",
                        "-122.200047",
                        "-122.199947"
                    ],
                    "lat": "47.6204774",
                    "lon": "-122.199997",
                    "display_name": "The UPS Store, 1100, Bellevue Way Northeast, Bellevue, King County, Washington, 98004, United States",
                    "class": "amenity",
                    "type": "post_office",
                    "importance": 0.53001,
                    "alternate_results": [
                        {
                            "place_id": 288749055,
                            "licence": "Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright",
                            "osm_type": "node",
                            "osm_id": 1987569546,
                            "boundingbox": [
                                "47.6204239",
                                "47.6205239",
                                "-122.2001916",
                                "-122.2000916"
                            ],
                            "lat": "47.6204739",
                            "lon": "-122.2001416",
                            "display_name": "AAA Cruises and Travel, 1100, Bellevue Way Northeast, Bellevue, King County, Washington, 98004, United States",
                            "class": "club",
                            "type": "automobile",
                            "importance": 0.53001
                        },
                        {
                            "place_id": 288749230,
                            "licence": "Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright",
                            "osm_type": "node",
                            "osm_id": 1987569543,
                            "boundingbox": [
                                "47.620366",
                                "47.620466",
                                "-122.201487",
                                "-122.201387"
                            ],
                            "lat": "47.620416",
                            "lon": "-122.201437",
                            "display_name": "Adventure Kids Playcare, 1100, Bellevue Way Northeast, Bellevue, King County, Washington, 98004, United States",
                            "class": "leisure",
                            "type": "playground",
                            "importance": 0.53001
                        }
                    ]
                }]}}


class GeoAPIReverseResponse(BaseModel):
    place_id: int
    licence: str
    osm_type: str
    osm_id: int
    lat: str
    lon: str
    display_name: str
    address: Dict[str, str]
    boundingbox: List[str]
    model_config = {
        "extra": "allow",
        "json_schema_extra": {
            "examples": [
                {
                    "place_id": 288417123,
                    "licence": "Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright",
                    "osm_type": "way",
                    "osm_id": 325822620,
                    "lat": "47.68148615",
                    "lon": "-122.20873015166683",
                    "display_name": "807, 1st Street, Juanita, Kirkland, King County, Washington, 98033, United States",
                    "address": {
                        "house_number": "807",
                        "road": "1st Street",
                        "suburb": "Juanita",
                        "town": "Kirkland",
                        "county": "King County",
                        "state": "Washington",
                        "ISO3166-2-lvl4": "US-WA",
                        "postcode": "98033",
                        "country": "United States",
                        "country_code": "us"
                    },
                    "boundingbox": [
                        "47.6814167",
                        "47.6815308",
                        "-122.2088759",
                        "-122.2086379"
                    ]
                }]}}
