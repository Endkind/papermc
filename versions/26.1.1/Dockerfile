FROM python:3.13-slim AS build

ARG VERSION=26.1.1
ARG BUILD=latest

COPY get-papermc.py get-papermc.py
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN python get-papermc.py --version $VERSION --build $BUILD --output /endkind/server.jar

FROM eclipse-temurin:latest AS runtime

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
ENV MINECRAFT_EULA=false
ENV JAVA_FLAGS="--add-modules=jdk.incubator.vector -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20"
ENV PAPERMC_FLAGS="--nojline"

USER papermc

ENTRYPOINT [ "/endkind/entrypoint.sh" ]
