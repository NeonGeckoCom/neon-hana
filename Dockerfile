FROM python:3.9-slim

LABEL vendor=neon.ai \
    ai.neon.name="neon-hana"

ENV OVOS_CONFIG_BASE_FOLDER neon
ENV OVOS_CONFIG_FILENAME diana.yaml
ENV XDG_CONFIG_HOME /config

RUN apt update && apt install -y swig gcc libpulse-dev

COPY docker_overlay/ /

WORKDIR /app
COPY . /app

RUN pip install /app[websocket,streaming]

CMD ["python3", "/app/neon_hana/app/__main__.py"]