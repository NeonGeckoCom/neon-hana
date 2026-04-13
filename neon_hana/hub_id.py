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

"""Generate memorable, Docker-style hub identifiers.

Produces kebab-case names like "bright-silver-falcon" or
"calm-amber-river-stone" that are easier to remember than UUIDs
when a user needs to identify which Hub they're connected to.
"""

import secrets

# 82 adjectives — evocative, whimsical, deliberately nonsequitur
# paired with tech nouns for maximum personality.
# Pruned: adjectives that are too specifically plant/terrain
# (mossy, pine, cedar, fern, oaken, marsh, timber, willow, rowan, etc.)
# The test: does "[adjective]-synapse" sound cool or silly?
_ADJECTIVES = [
    "ancient", "amber", "arctic", "azure", "bold", "brave", "bright",
    "bronze", "calm", "clear", "clever", "cobalt", "coral", "cosmic",
    "crisp", "crystal", "daring", "dawn", "deep", "eager", "ember",
    "fair", "fierce", "frost", "gentle", "gilded", "glad", "golden",
    "grand", "hidden", "hollow", "iron", "ivory", "jade", "keen",
    "kind", "lapis", "light", "lilac", "lively", "lunar", "marble",
    "merry", "noble", "north", "onyx", "opal", "pale", "pearl",
    "plain", "plum", "polar", "proud", "quiet", "rapid", "ruby",
    "scarlet", "serene", "shadow", "sharp", "silent", "silver", "slate",
    "solar", "south", "steady", "steel", "still", "storm", "sunny",
    "swift", "tawny", "teal", "tender", "topaz", "true", "velvet",
    "vivid", "warm", "west", "wild", "wise",
]

# 73 nouns — AI, computing, science, engineering
_NOUNS = [
    "agent", "array", "aurora", "batch", "beacon", "cache", "charge",
    "cipher", "circuit", "codec", "coil", "core", "cortex", "diode",
    "echo", "epoch", "field", "flux", "forge", "gate", "glyph",
    "graph", "grid", "helix", "index", "kernel", "laser", "lattice",
    "lens", "link", "loom", "matrix", "mesh", "model", "modem",
    "neuron", "nexus", "node", "optic", "orbit", "parse", "patch",
    "phase", "photon", "pixel", "plasma", "probe", "prism", "pulse",
    "qubit", "radar", "relay", "rotor", "scope", "servo", "shard",
    "signal", "socket", "sonar", "spark", "stack", "switch", "sync",
    "synapse", "tensor", "token", "trace", "valve", "vector", "vertex",
    "voxel", "watt", "wave",
]


_rng = secrets.SystemRandom()


def generate_hub_id() -> str:
    """Generate a three-word kebab-case identifier.

    Format: adjective-adjective-noun (adjectives are always distinct)
    Combinatorial space: 82 * 81 * 73 ≈ 485K unique IDs.
    Collision probability is negligible for home networks.
    """
    adj1, adj2 = _rng.sample(_ADJECTIVES, 2)
    noun = _rng.choice(_NOUNS)
    return f"{adj1}-{adj2}-{noun}"
