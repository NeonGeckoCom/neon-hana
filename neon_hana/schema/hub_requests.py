# NEON AI (TM) SOFTWARE, Software Development Kit & Application Development System
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2026 Neongecko.com Inc.
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

from pydantic import BaseModel, Field, field_validator


class TTSConfig(BaseModel):
    """TTS plugin configuration."""

    module: str = Field(description="Active TTS plugin module name")


class STTConfig(BaseModel):
    """STT plugin configuration."""

    module: str = Field(description="Active STT plugin module name")


class LLMConfig(BaseModel):
    """LLM configuration."""

    name: str = Field(description="Active LLM engine name")


class HubConfigResponse(BaseModel):
    """Response model for GET /hub/config."""

    tts: Optional[TTSConfig] = Field(
        default=None,
        description="Active TTS configuration, or null if unavailable",
    )
    stt: Optional[STTConfig] = Field(
        default=None,
        description="Active STT configuration, or null if unavailable",
    )
    llm: LLMConfig = Field(description="Active LLM configuration")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "tts": {"module": "neon-tts-plugin-coqui"},
                    "stt": {"module": "neon-stt-plugin-nemo"},
                    "llm": {"name": "Neon Classic"},
                }
            ]
        }
    }


class HubIdentityResponse(BaseModel):
    """Response model for GET /hub/identity."""

    hub_id: str = Field(description="Stable, human-readable hub identifier (e.g. 'bright-silver-falcon')")
    display_name: str = Field(description="User-configurable display name for this hub")
    version: str = Field(description="HANA software version")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "hub_id": "bright-silver-falcon",
                    "display_name": "Neon Hub (Office)",
                    "version": "0.1.1a21",
                }
            ]
        }
    }


class UpdateHubIdentityRequest(BaseModel):
    """Request model for POST /hub/identity."""

    display_name: str = Field(min_length=1, max_length=128, description="New display name for this hub")

    @field_validator("display_name")
    @classmethod
    def strip_and_validate(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("display_name must not be blank")
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "display_name": "Kitchen Hub",
                }
            ]
        }
    }
