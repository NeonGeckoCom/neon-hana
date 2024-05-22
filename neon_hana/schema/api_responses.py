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
    minutely: Optional[List[dict]]
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
                    "provider": "alpha_vantage",
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
                    "provider": "alpha_vantage",
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


class WolframAlphaAPIResponse(BaseModel):
    answer: str
    model_config = {
        "extra": "allow",
        "json_schema_extra": {
            "examples": [
                {
                    "answer": "The distance from Earth to the Moon at 4:29 P.M. Pacific Standard Time, Friday, January 12, 2024 is about 225192 miles"
                }, {
                    "answer": "about 5378 miles"
                }, {
                    "answer": "<?xml version='1.0' encoding='UTF-8'?>\n<queryresult success='false'\n    error='true'\n    xml:space='preserve'\n    numpods='0'\n    datatypes=''\n    timedout=''\n    timedoutpods=''\n    timing='0.015'\n    parsetiming='0.'\n    parsetimedout='false'\n    recalculate=''\n    id=''\n    parseidserver='15'\n    host='https://www6b3.wolframalpha.com'\n    server='15'\n    related=''\n    version='2.6'\n    inputstring=''>\n <error>\n  <code>1000</code>\n  <msg>input parameter not present in query</msg>\n </error>\n</queryresult>"
                }]}}


class ScriptParserResponse(BaseModel):
    ncs: str
    model_config = {
        "extra": "allow",
        "json_schema_extra": {
            "examples": [{
                "ncs": "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KZRoBksAaAdomGgJXZR1fZQoaANLPWgEjA5MT09QIGNoZWNrIEVORJRoBksAaAdqAgEAAGgJXZR1fZQoaANLPmgEjEwiTWFpbCBUaXRsZSIsICJlbWFpbCBib2R5IGdvZXMgaGVyZS4gY291bGQgYmUgYSB2YXJpYWJsZSBuYW1lIGluIG1vc3QgY2FzZXMilGgGSwBoB4wFZW1haWyUaAldlGgLfZQojAdzdWJqZWN0lIwMIk1haWwgVGl0bGUilIwEYm9keZSMPiJlbWFpbCBib2R5IGdvZXMgaGVyZS4gY291bGQgYmUgYSB2YXJpYWJsZSBuYW1lIGluIG1vc3QgY2FzZXMilHV1fZQoaANLP2gEjBBzY3JpcHRfbmFtZV9oZXJllGgGSwBoB4wDcnVulGgJXZRoC32UjA1zY3JpcHRfdG9fcnVulGomAQAAc3V9lChoA0tAaASMBEV4aXSUaAZLAGgHjARleGl0lGgJXZR1ZX2UKGh7aHxoWWheaFxoXYwNb3ZlcnJpZGVfdXNlcpSIdX2UKGhgTmhuTnV9lIwFY2hlY2uUfZQojAVzdGFydJRLOIwDZW5klEs9dXN9lGiQSx1zSxROXZQoaDxoQmhIZX2UKGhOaFBoVWhWdX2UKIwIY3ZlcnNpb26UjAUwLjUuMJSMCGNvbXBpbGVklEpc6qFljAhjb21waWxlcpSMFU5lb24gQUkgU2NyaXB0IFBhcnNlcpRoDWgFaBBoD2gVjE8KSnVzdCBhbiBleGFtcGxlIGRlc2NyaXB0aW9uIHRvIGdvIHdpdGgKYW4gZXhhbXBsZSBzY3JpcHQuIFRoaXMgd2lsbCBnbyBpbiBtZXRhlIwIcmF3X2ZpbGWUWEAFAAAKU2NyaXB0OiBQYXJzZXIgVGVzdCBTY3JpcHQKQXV0aG9yOiBEYW5pZWwgTWNLbmlnaHQKRGVzY3JpcHRpb246CiAgICBKdXN0IGFuIGV4YW1wbGUgZGVzY3JpcHRpb24gdG8gZ28gd2l0aAogICAgYW4gZXhhbXBsZSBzY3JpcHQuIFRoaXMgd2lsbCBnbyBpbiBtZXRhCgojIFRpbWVvdXQgZ290byBsaW5lIDE4ClRpbWVvdXQ6IDEwLCAxOAojIFRpbWVvdXQgZXhpdApUaW1lb3V0OiAyMAoKU3lub255bTogIlRlc3QgU2NyaXB0IgogICAgIlRlc3RlciBTY3JpcHQiCiAgICAiQW5vdGhlciBTeW5vbnltIgpDbGFwczogMiBUd28gY2xhcCBhY3Rpb24KICAgIDMgMyBjbGFwIGFjdGlvbgpMYW5ndWFnZTogZW4tdXMsIG1hbGUKClZhcmlhYmxlOiBub192YWwKVmFyaWFibGU6IHdpdGhfdmFsID0gIlRlc3QgVmFsdWUiCgojIFRoaXMgaXMgYSBjb21tZW50IGxpbmUgc2VwYXJhdGluZyBoZWFkZXIgZnJvbSBleGVjdXRpb24gKGtpbmRhKQpOZW9uIHNwZWFrOiBpbmxpbmVkIHNwZWFrCk5lb24gc3BlYWs6CiAgICBCbG9jayBzcGVlY2ggc3RhcnQKICAgIC4uLgogICAgQmxvY2sgc3BlZWNoIGVuZApAcHJlLWV4ZWMKRXhlY3V0ZTogaGVsbG8gd29ybGQKdm9pY2VfaW5wdXQobm9fdmFsKQpJRiBub192YWwgPT0gd2l0aF92YWw6CiAgICBHb3RvOiBwcmUtZXhlYwpFTFNFOgogICAgUmVjb252ZXk6IHByZS1leGVjCgpJZiAid29yZCIgSU4gInRoaXMgcGhyYXNlIHdvcmQgaXMgaW4iOgogICAgTmVvbiBzcGVhazogInBocmFzZSIKClJlY29udmV5OiBwcmUtZXhlYywgZmlsZV9wYXJhbQpOYW1lIFJlY29udmV5OiAiU29tZW9uZSIsICJzb21lIHRleHQiLCAiL3BhdGgvdG8vZmlsZSIKCkNhc2Uge3dpdGhfdmFsfToKICAgICJTb21lIHZhbHVlIgogICAgICAgIE5lb24gc3BlYWs6IGZpcnN0CiAgICAic29tZSBvdGhlciB2YWx1ZSIKICAgICAgICBOZW9uIHNwZWFrOgogICAgICAgICAgICBzZWNvbmQKCkNhc2Uobm9fdmFsKToKICAgICJub192YWxfMSI6CiAgICAgICAgRXhlY3V0ZTogd2hhdCB0aW1lIGlzIGl0CgpQeXRob246IDEqMiAgIyBUT0RPOiBzeW50YXggY2hlY2sKCkxPT1AgY2hlY2sgU1RBUlQKU2V0OiBuZXdfdmFsID0gbm9fdmFsICAjIFRoaXMgbG9ncyBhbiBlcnJvciBiZWNhdXNlIGl0IGlzbid0IGRlY2xhcmVkCiMgVE9ETzogVGhlIGZvbGxvd2luZyBzaG91bGQgd2Fybi9lcnJvcgpkbmUgPSAidGVzdCIKdm9pY2VfaW5wdXQobmV3X3ZhbCkKTE9PUCBjaGVjayBFTkQKRW1haWw6ICJNYWlsIFRpdGxlIiwgImVtYWlsIGJvZHkgZ29lcyBoZXJlLiBjb3VsZCBiZSBhIHZhcmlhYmxlIG5hbWUgaW4gbW9zdCBjYXNlcyIKUnVuOiBzY3JpcHRfbmFtZV9oZXJlCkV4aXSUdX2UKGhgaGdobmhwdWUu"
            }]}}


class CouponsResponse(BaseModel):
    success: bool
    brands: List[str]
    coupons: List[str]

    model_config = {
        "extra": "allow",
        "json_schema_extra": {
            "examples": [{
                "success": True,
                "brands": [
                    "amazon",
                    "blue apron",
                    "home depot",
                    "old navy",
                    "bed bath and beyond",
                    "sears",
                    "dominos",
                    "budget car rental",
                    "orbitz",
                    "target",
                    "kohls",
                    "nordstrom",
                    "amazon prime now",
                    "apple",
                    "google",
                    "coca cola",
                    "microsoft",
                    "mycroft",
                    "samsung",
                    "ebikes",
                    "kroll maps",
                    "brand",
                    "harrypotter",
                    "conversation processing intelligence",
                    "value added websites",
                    "neon",
                    "steve jones",
                    "alpha",
                    "beta",
                    "gamma",
                    "december",
                    "strata",
                    "intelligent",
                    "flower",
                    "argon",
                    "steve",
                    "elon 5000",
                    "theta",
                    "pool",
                    "josh",
                    "test",
                    "grass",
                    "testing",
                    "demo",
                    "mack",
                    "june",
                    "door dash",
                    "newegg",
                    "amtrak",
                    "toms",
                    "graco",
                    "otterbox",
                    "auto zone",
                    "uber",
                    "papa johns",
                    "bed bath and beyond",
                    "target",
                    "macys",
                    "best buy",
                    "dominos",
                    "office depot",
                    "kohls",
                    "bath and body works",
                    "best buy",
                    "budget rental car",
                    "carters",
                    "dicks sporting goods",
                    "door dash",
                    "enterprise rental car",
                    "famous footware",
                    "fashion nova",
                    "home depot",
                    "hotels.com",
                    "jcpenney",
                    "michaels",
                    "old navy",
                    "oriental trading company",
                    "pizza hut",
                    "post mates",
                    "sephora",
                    "shutterfly",
                    "southwest airlines",
                    "uber eats",
                    "ulta",
                    "victorias secret",
                    "spirit airlines",
                    "rock auto",
                    "vistaprint",
                    "panera bread",
                    "ebay",
                    "walgreens",
                    "revolve",
                    "priceline",
                    "hotels.com",
                    "1800flowers",
                    "airbnb",
                    "staples",
                    "jet.com",
                    "dell.com",
                    "jomashop",
                    "rakuten",
                    "walmart",
                    "groupon",
                    "barnes and noble",
                    "new york times",
                    "old navy",
                    "sprint",
                    "delta",
                    "alaska air",
                    "ford",
                    "mcdonalds",
                    "taco bell",
                    "red lobster",
                    "olive garden",
                    "olive garden",
                    "applebees",
                    "starbucks",
                    "target",
                    "bed bath and beyond",
                    "ticketmaster",
                    "airbnb",
                    "dominos",
                    "papa johns",
                    "door dash",
                    "ashley home store",
                    "august"
                ],
                "coupons": [
                    "\"1800flowers\",\"20% Off Flowers And Gifts\",\"SAVETWENTY\"",
                    "\"airbnb\",\"Save 10% on your AirBnB booking\",\"SAVE10\"",
                    "\"airbnb\",\"$40 off your booking with Airbnb\",\"dsenter10\"",
                    "\"alaska air\",\"5% Off Flights For Insider Members\",\"EC6208\"",
                    "\"alpha\",\"Save 10% off with Alpha Brand!\",\"ALF10\"",
                    "\"amazon\",\"NEW CUSTOMERS! $10 OFF YOUR FIRST PRIME NOW ORDER.\",\"10PRIMENOW\"",
                    "\"amazon prime now\",\"Up to $20 Off Your First Orders Through Prime Now Or Whole Foods Market\",\"20PRIMEDAY\"",
                    "\"amtrak\",\"Buy One Ticket, Get One Free When You Share a Bedroom or Roomette\",\"V540\"",
                    "\"apple\",\"$5 Cash Back on $50 for Beats, iPods, and Accessories\",\"ONLINE\"",
                    "\"applebees\",\"$5 Off $25+ Your First Online Order\",\"5OFF25\"",
                    "\"argon\",\"Save 10% on Argon\",\"Argon10off\"",
                    "\"ashley home store\",\"Up to 70% Off + Extra 10% Off + 12 Months Special Financing\",\"POPUP19\"",
                    "\"auto zone\",\"10% on Auto Zone Orders Online or In store\",\"NGZone\"",
                    "\"barnes and noble\",\"25% Off All Eligible NOOK Book Bash Items With Coupon Code\",\"NOOKBASH25\"",
                    "\"bath and body works\",\"20% Off With Promo Code online\",\"TWYSURT\"",
                    "\"bed bath and beyond\",\"20% Off One Item In-Store\",\"20OFFBBB\"",
                    "\"bed bath and beyond\",\"20% Off online orders\",\"20OFF\"",
                    "\"bed bath and beyond\",\"Save 20% off when you sign up for emails.\",\"None needed\"",
                    "\"best buy\",\"Save 20% on regular-priced appliances with promo code\",\"SAVEONSMALLSNOW\"",
                    "\"best buy\",\"20% Off one regular priced item\",\"APPLY20RMNNOW\"",
                    "\"beta\",\"Save 20% off BETA and free shipping\",\"BETA20\"",
                    "\"blue apron\",\"$30 OFF YOUR FIRST DELIVERY!\",\"BA17B25\"",
                    "\"brand\",\"A 1-2-3 Punch of savings\",\"Brand123\"",
                    "\"budget car rental\",\"Up to $25 Off Base Rate on your Car Rental with Minimum Spend\",\"MUWZ092\"",
                    "\"budget rental car\",\"$40 Off Intermediate Or Larger Vehicle Rent\",\"MUGZ025\"",
                    "\"carters\",\"Extra 20% Off Your $50+ In-Store Purchase\",\"CART20\"",
                    "\"coca cola\",\"GET REWARDED WHEN YOU BUY COKE PRODUCTS\",\"REWARDS\"",
                    "\"conversation processing intelligence\",\"Get free conversation transcription\",\"CPI180822\"",
                    "\"december\",\"Get 10% off in December\",\"DECEMBER10\"",
                    "\"dell.com\",\"15% off site wide\",\"SAVE15\"",
                    "\"delta\",\"Up to $250 Off Summer Vacation Bookings To The Caribbean + Earn 2,500 Extra Bonus Miles Per Person\",\"DVSUMMERA\"",
                    "\"demo\",\"Save 10% off demo\",\"Demo10\"",
                    "\"dicks sporting goods\",\"Extra 10% Off Next Purchase With Dick's Sporting Goods Email Sign Up\",\"No Code needed\"",
                    "\"dominos\",\"Carryout Large 3-Topping Pizza for $7.99\",\"9174\"",
                    "\"dominos\",\"30% off Large Traditional & Premium Pizzas, Pick up or Delivered\",\"355852\"",
                    "\"dominos\",\"40% off your order of regular priced pizza\",\"222233\"",
                    "\"door dash\",\"$5 off $10 on Pickup Orders\",\"PICKUPTIME\"",
                    "\"door dash\",\"$5 Off $15\",\"NOVDASH18\"",
                    "\"door dash\",\"$15 off your order\",\"FSt4vk\"",
                    "\"ebay\",\"$5 Off Your Order For New Users\",\"WELCOME5\"",
                    "\"ebikes\",\"10% off ebike kit #1\",\"EB01\"",
                    "\"elon 5000\",\"Brightest mind in the Northwest\",\"XYZ\"",
                    "\"enterprise rental car\",\"10 Off when you book a luxury car\",\"10Off\"",
                    "\"famous footware\",\"$10 Off Your Orders of $50+\",\"ENTR2018\"",
                    "\"fashion nova\",\"30% Off Your Fashion Nova Purchase + Free Shipping Over $75\",\"NOVABABE5-56NS46\"",
                    "\"flower\",\"Save 10% off all flowers!\",\"Flower10\"",
                    "\"ford\",\"10% Off Sitewide\",\"FORDSUMMER14\"",
                    "\"gamma\",\"save on all of your GAMMA needs!\",\"GAMMA30\"",
                    "\"google\",\"$15 off your purchase WITH GOOGLE EXPRESS\",\"KGUCT33MF\"",
                    "\"graco\",\"20% Off Sitewide (Excluding 4Ever)\",\"SUMMEROFGRACO\"",
                    "\"grass\",\"Save 10% off Grass\",\"Grass10\"",
                    "\"groupon\",\"SAVE10\",\"$10 off your order\"",
                    "\"guy's ebikes\",\"20% off\",\"EB1\"",
                    "\"harrypotter\",\"Get a free wizard!\",\"HarryPotterWizard\"",
                    "\"home depot\",\"Additional 10% Off Cutlery Items And Accessories\",\"CHOPUPSAVINGS\"",
                    "\"home depot\",\"$5 Off Coupon With Home Depot Email Signup\",\"No Coupon Code\"",
                    "\"hotels.com\",\"Extra 10% Off Select Hotels\",\"RC10\"",
                    "\"hotels.com\",\"Extra 10% Off Select Hotels\",\"WEDDING10\"",
                    "\"intelligent\",\"SAve 10% off intelligent devices\",\"Intelligent10\"",
                    "\"jcpenney\",\"20% In Store and Online\",\"GIFTDAD\"",
                    "\"jet.com\",\"30% off all Grocery Pup items\",\"GROCERYPUP\"",
                    "\"jomashop\",\"$10 off orders of $150\",\"AD10\"",
                    "\"josh\",\"Josh saves 10%\",\"Josh10\"",
                    "\"june\",\"save 10% on June! Wow!\",\"JUNE10\"",
                    "\"kohls\",\"Save an Extra 20% Off\",\"FIREWORK\"",
                    "\"kohls\",\"15% Off $100 or More + Free Shipping\",\"CATCH15OFF\"",
                    "\"kroll maps\",\"20% off all European Maps!!!\",\"KR01\"",
                    "\"mack\",\"Save 10% off all MAck products\",\"Mack10\"",
                    "\"macys\",\"30% Off Lauren Ralph Lauren\",\"FRIEND\"",
                    "\"mcdonalds\",\"McDonald's Offers, Codes, In-store Coupons, And More\",\"Sign up in App\"",
                    "\"michaels\",\"50% Off One Regular-Priced Item With Michaels Coupon\",\"50HALFBDAY\"",
                    "\"microsoft\",\"10% off + Free shipping for students and parents\",\"10% OFF\"",
                    "\"mycroft\",\"KICKSTARTER - Pledge $299 or more 3-Pack of Mark II devices\",\"MARKII -\"",
                    "\"neon\",\"Save 20% when you buy a NeonX 10 inch audio pc.\",\"NeonXSave20\"",
                    "\"new york times\",\"15% Off Orders Over $50\",\"MOM15\"",
                    "\"newegg\",\"5% Off $50+ on Select CPUs, Input Devices & More\",\"CORNSAVE519\"",
                    "\"nordstrom\",\"Free 21-Piece Gift With Your $75 Beauty Or Fragrance Purchase\",\"TEAL\"",
                    "\"office depot\",\"20% Off Your Qualifying  Regular Priced Purchase\",\"DMXP6\"",
                    "\"old navy\",\"OHYES\",\"ohyes\"",
                    "\"old navy\",\"20% Off Sitewide\",\"SWEET\"",
                    "\"old navy\",\"20% Off Your Purchase With Old Navy Email Sign-up\",\"No Code needed\"",
                    "\"olive garden\",\"Free Appetizer Or Dessert With Olive Garden Email Signup\",\"No Code needed\"",
                    "\"olive garden\",\"$2 Off 2 Lunches\",\"2OFF2L\"",
                    "\"orbitz\",\"15% Off Select Hotels\",\"HEATWAVE\"",
                    "\"oriental trading company\",\"Up to $40 Off + Free Shipping on $49\",\"6SAVENOW\"",
                    "\"otterbox\",\"10% off\",\"ULTIMATE10\"",
                    "\"panera bread\",\"50% Off Orders $25+ For Rapid Pick-Up Order\",\"MMDRF\"",
                    "\"papa johns\",\"30% Off Regular Menu-Priced Orders\",\"GET30\"",
                    "\"papa johns\",\"30% Off Regular Menu-Priced Orders with Promo Code!\",\"GET30\"",
                    "\"pizza hut\",\"BF9VY9VE4XE2\",\"BF9VY9VE4XE2\"",
                    "\"pool\",\"save on your pool!\",\"pool10\"",
                    "\"post mates\",\"$100 in delivery credits\",\"FOOD4YOU\"",
                    "\"priceline\",\"8% Off Select Hotels\",\"RMNJUN8\"",
                    "\"rakuten\",\"20% Clothing, Shoes and Accessories\",\"APPAREL20\"",
                    "\"red lobster\",\"10% Off Any To Go Order\",\"LOBSTER75\"",
                    "\"revolve\",\"20% Off Sitewide\",\"REVOLVE4AU\"",
                    "\"rock auto\",\"5% off your order\",\"10703653554843330\"",
                    "\"samsung\",\"$100 Off Samsung POWERbot Robot Vacuum + Additional $50 Off + Free Shipping\",\"PLXGUA9Z7\"",
                    "\"sears\",\"Extra $35 Off $300+ on Home Appliances, Lawn & Garden, Tools, Mattresses & Sporting Goods\",\"SEARS35OFF300\"",
                    "\"sephora\",\"FREE gift with select purchase online only\",\"PICKYOURS\"",
                    "\"shutterfly\",\"30% Off Sitewide\",\"30SAVINGS\"",
                    "\"southwest airlines\",\"Up to 35% Off Base Rate For Hertz Rentals + Up to 2400 Rapid Rewards Points\",\"159062\"",
                    "\"spirit airlines\",\"$50 off bookings\",\"CD50\"",
                    "\"sprint\",\"50% Off When You Upgrade\",\"No Code needed\"",
                    "\"staples\",\"$15 Off Orders of $100+\",\"67914\"",
                    "\"starbucks\",\"$5 Gift With Your Order\",\"wjmnm\"",
                    "\"steve\",\"Test of Steve\",\"test\"",
                    "\"steve jones\",\"Free Call From Steve\",\"steve\"",
                    "\"strata\",\"save 10% off strata\",\"STRATA10\"",
                    "\"taco bell\",\"10% Off Online Order\",\"Save 10% when you order online\"",
                    "\"target\",\"$5 Off $50 Select Items + Free Shipping on Qualifying Purchases\",\"90209\"",
                    "\"target\",\"$5 Off $50 Select Items at Target + Free Shipping\",\"No Code needed\"",
                    "\"target\",\"$5 Off $50 Select Items at Target + Free Shipping\",\"FIVEOFF\"",
                    "\"test\",\"save 10% off test\",\"Test10\"",
                    "\"testing\",\"Save 10% off\",\"Test10\"",
                    "\"theta\",\"saave 10% off Theta\",\"theta10\"",
                    "\"ticketmaster\",\"Save 50% when you buy two tickets\",\"TMN241\"",
                    "\"toms\",\"$10 off any order and free shipping\",\"CHANGE\"",
                    "\"uber\",\"$5 off each of your first 3 trips\",\"NEWRIDER15\"",
                    "\"uber eats\",\"40% Off First Order\",\"SAVE40\"",
                    "\"ulta\",\"401534\",\"401534\"",
                    "\"value added websites\",\"100% off all new websites!\",\"VAW01\"",
                    "\"victorias secret\",\"FREE shipping on orders over $50\",\"SHIP50\"",
                    "\"vistaprint\",\"Up to 50% Off Everything Only at Vistaprint!\",\"SALE50\"",
                    "\"walgreens\",\"50% Off Prints ...\",\"COOLPIX\"",
                    "\"walmart\",\"$10 Off Orders $50+ at Walmart Grocery\",\"LA9ARAAC\""
                ]}]}}
