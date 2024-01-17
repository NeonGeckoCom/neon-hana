FROM python:3.9-slim

LABEL vendor=neon.ai \
    ai.neon.name="diana-services-api"

ENV OVOS_CONFIG_BASE_FOLDER neon
ENV OVOS_CONFIG_FILENAME diana.yaml
ENV XDG_CONFIG_HOME /config

COPY docker_overlay/ /

WORKDIR /app
COPY . /app
RUN pip install /app

CMD ["python3", "/app/diana_services_api/app/__main__.py"]