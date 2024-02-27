# HANA
HANA (HTTP API for Neon Applications) provides a unified front-end for 
accessing services in a [Neon DIANA](https://github.com/NeonGeckoCom/neon-diana-utils) deployment. This API should generally 
be hosted as part of a Diana deployment to safely expose services to outside
traffic.

Full API documentation is automatically generated and accessible at `/docs`.

## Configuration
User configuration belongs in `diana.yaml`, mounted in the container path 
`/config/neon/`. An example user configuration could be:
```yaml
MQ:
  server: mq.mydomain.com
hana:
  mq_default_timeout: 10
  access_token_ttl: 86400  # 1 day
  refresh_token_ttl: 604800  # 1 week
  requests_per_minute: 60
  auth_requests_per_minute: 6  # This counts valid and invalid requests from an IP address
  access_token_secret: a800445648142061fc238d1f84e96200da87f4f9fa7835cac90db8b4391b117b
  refresh_token_secret: 833d369ac73d883123743a44b4a7fe21203cffc956f4c8fec712e71aafa8e1aa
  fastapi_title: "My HANA API Host"
  fastapi_summary: "Personal HTTP API to access my DIANA backend."
  disable_auth: True
  stt_max_length_encoded: 500000  # Arbitrary limit that is larger than any expected voice command
  tts_max_words: 128  # Arbitrary limit that is longer than any default LLM token limit
  enable_email: True  # Disabled by default; anyone with access to the API will be able to send emails from the configured address

```
It is recommended to generate unique values for configured tokens, these are 32
bytes in hexadecimal representation.

## Deployment
You can build a Docker container from this repository, or pull a built container
from the GitHub Container Registry. Start Hana via:
```shell
docker run -p 8080:8080 -v ~/.config/neon:/config/neon ghcr.io/neongeckocom/neon-hana
```
> This assumes you have configuration defined in `~/.config/neon/diana.yaml` and
  are using the default port 8080

## Usage
Full API documentation is available at `/docs`. The `/auth/login` endpoint should
be used to generate a `client_id`, `access_token`, and `refresh_token`. The
`access_token` should be included in every request and upon expiration of the
`access_token`, a new token can be obtained from the `auth/refresh` endpoint.
