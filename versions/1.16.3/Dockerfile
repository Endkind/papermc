FROM python:3.13-slim AS build

ARG VERSION=1.16.3
ARG BUILD=latest

COPY get-papermc.py get-papermc.py
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN python get-papermc.py --version $VERSION --build $BUILD --output /endkind/server.jar

FROM eclipse-temurin:11 AS runtime

LABEL Author="Endkind Ender <endkind.ender@endkind.net>"

RUN groupadd --system --gid 10001 papermc \
    && useradd --system --uid 10001 --gid papermc --home-dir /data --shell /usr/sbin/nologin papermc \
    && mkdir -p /endkind /data \
    && chown -R papermc:papermc /endkind /data

COPY --chown=papermc:papermc entrypoint.sh /endkind/entrypoint.sh
RUN chmod +x /endkind/entrypoint.sh

COPY --from=build --chown=papermc:papermc /endkind/server.jar /endkind/server.jar

WORKDIR /data
VOLUME /data

ENV MIN_RAM=512M
ENV MAX_RAM=3G
ENV JAVA_FLAGS=""
ENV PAPERMC_FLAGS="--nojline"

USER papermc

ENTRYPOINT [ "/endkind/entrypoint.sh" ]
