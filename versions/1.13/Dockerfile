FROM python:3.13-slim AS build

ARG VERSION=1.13
ARG BUILD=latest

COPY get-papermc.py get-papermc.py
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN python get-papermc.py --version $VERSION --build $BUILD --output /endkind/server.jar

FROM rust:1.94.0-slim AS healthcheck-build

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates \
    && TAG=$(git ls-remote --tags --sort="v:refname" https://github.com/Endkind/MinecraftHealthCheck.git | grep -v '\^{}' | tail -n 1 | cut -d/ -f3-) \
    && git clone --depth 1 --branch "$TAG" https://github.com/Endkind/MinecraftHealthCheck.git . \
    && cargo build --release \
    && rm -rf /var/lib/apt/lists/*

FROM eclipse-temurin:11 AS runtime

LABEL Author="Endkind Ender <endkind.ender@endkind.net>"

RUN groupadd --system --gid 10001 papermc \
    && useradd --system --uid 10001 --gid papermc --home-dir /data --shell /usr/sbin/nologin papermc \
    && mkdir -p /endkind /data \
    && chown -R papermc:papermc /endkind /data

COPY --chown=papermc:papermc \
    entrypoint.sh \
    /endkind/entrypoint.sh
COPY --from=build \
    --chown=papermc:papermc \
    /endkind/server.jar \
    /endkind/server.jar
COPY --from=healthcheck-build \
    --chown=papermc:papermc \
    /build/target/release/MinecraftHealthCheck \
    /endkind/healthcheck

RUN chmod +x \
    /endkind/entrypoint.sh \
    /endkind/healthcheck

WORKDIR /data
VOLUME /data

ENV MIN_RAM=512M
ENV MAX_RAM=3G
ENV JAVA_FLAGS=""
ENV PAPERMC_FLAGS="--nojline"

USER papermc

HEALTHCHECK \
    --interval=60s \
    --timeout=60s \
    --start-period=60s \
    --retries=1 \
    CMD ["/endkind/healthcheck"]

ENTRYPOINT [ "/endkind/entrypoint.sh" ]
