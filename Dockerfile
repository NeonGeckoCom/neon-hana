FROM python:3.11-slim

LABEL vendor=neon.ai \
    ai.neon.name="neon-hana"

ENV OVOS_DEFAULT_CONFIG=/opt/neon/diana.yaml
ENV OVOS_CONFIG_BASE_FOLDER=neon
ENV OVOS_CONFIG_FILENAME=diana.yaml
ENV XDG_CONFIG_HOME=/config

RUN apt-get update && \
    apt-get install -y \
    swig \
    gcc \
    libpulse-dev \
    portaudio19-dev \
    curl

COPY docker_overlay/ /

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir /app[websocket,streaming]

HEALTHCHECK CMD "/opt/neon/healthcheck.sh"
CMD ["python3", "/app/neon_hana/app/__main__.py"]
