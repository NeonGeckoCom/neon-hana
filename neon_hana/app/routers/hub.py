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

import os
from typing import Optional

import yaml
from fastapi import APIRouter, Depends
from ovos_config.config import update_mycroft_config
from ovos_utils.log import LOG

from neon_hana.app.dependencies import config, jwt_bearer
from neon_hana.hub_id import generate_hub_id
from neon_hana.schema.hub_requests import (
    HubConfigResponse,
    HubIdentityResponse,
    LLMConfig,
    STTConfig,
    TTSConfig,
    UpdateHubIdentityRequest,
)
from neon_hana.version import __version__

_DEFAULT_TTS_MODULE = "neon-tts-plugin-coqui"
_DEFAULT_STT_MODULE = "neon-stt-plugin-nemo"

hub_route = APIRouter(prefix="/hub", tags=["hub"])

# Generate hub_id eagerly at import time to avoid a race condition
# where two concurrent first-boot requests each generate a different ID.
_hub_id = config.get("hub_id")
if not _hub_id:
    _hub_id = generate_hub_id()
    LOG.info("Generated new hub_id: %s", _hub_id)
    update_mycroft_config({"hana": {"hub_id": _hub_id}})
    config["hub_id"] = _hub_id


@hub_route.get("/identity")
async def get_hub_identity() -> HubIdentityResponse:
    """
    Get the identity of this Hub.

    Returns a stable hub ID, user-configurable display name, and
    software version. This endpoint is public (no authentication
    required) so that Nodes can identify a Hub during discovery.
    """
    display_name = config.get("hub_display_name") or "Neon Hub"
    return HubIdentityResponse(
        hub_id=_hub_id,
        display_name=display_name,
        version=__version__,
    )


@hub_route.post("/identity", dependencies=[Depends(jwt_bearer)])
async def update_hub_identity(
    request: UpdateHubIdentityRequest,
) -> HubIdentityResponse:
    """
    Update the display name of this Hub.

    Requires authentication. The new display name is persisted to
    the configuration file and survives container restarts.
    """
    update_mycroft_config({"hana": {"hub_display_name": request.display_name}})
    config["hub_display_name"] = request.display_name
    LOG.info("Hub display_name updated to: %s", request.display_name)
    return HubIdentityResponse(
        hub_id=_hub_id,
        display_name=request.display_name,
        version=__version__,
    )


def _read_neon_yaml() -> Optional[dict]:
    """Read neon.yaml from the XDG config path.

    Returns the parsed config dict, or None if the file is missing or
    unreadable (e.g. HANA running outside a Hub deployment, permission
    issues, or malformed YAML).
    """
    xdg_config = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
    neon_yaml_path = os.path.join(xdg_config, "neon", "neon.yaml")
    try:
        with open(neon_yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except FileNotFoundError:
        LOG.info("neon.yaml not found at %s", neon_yaml_path)
        return None
    except (PermissionError, IsADirectoryError, yaml.YAMLError) as e:
        LOG.warning("Failed to read neon.yaml at %s: %s", neon_yaml_path, e)
        return None
    if not isinstance(data, dict):
        LOG.warning("neon.yaml at %s is not a mapping (got %s); ignoring",
                     neon_yaml_path, type(data).__name__)
        return None
    return data


@hub_route.get("/config")
async def get_hub_config() -> HubConfigResponse:
    """
    Get the active configuration of this Hub.

    Returns the currently configured TTS, STT, and LLM engines.
    TTS/STT are read from neon.yaml on each request so that
    config changes are reflected without restarting HANA.
    If the file is not present (non-Hub deployment), those
    fields are null. If present but the keys are not set,
    known defaults are returned.

    This endpoint is public (no authentication required) so that
    Nodes can display Hub configuration during discovery.
    """
    neon_config = _read_neon_yaml()

    if neon_config is None:
        tts = None
        stt = None
    else:
        tts_module = (neon_config.get("tts") or {}).get("module", _DEFAULT_TTS_MODULE)
        stt_module = (neon_config.get("stt") or {}).get("module", _DEFAULT_STT_MODULE)
        tts = TTSConfig(module=tts_module)
        stt = STTConfig(module=stt_module)

    return HubConfigResponse(
        tts=tts,
        stt=stt,
        llm=LLMConfig(name="Neon Classic"),
    )
