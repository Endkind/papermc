FROM eclipse-temurin:18
RUN apt-get update && apt-get install -y \
    curl \
    jq

LABEL Author Endkind Ender <endkind.ender@endkind.net>

COPY getPaperMC.sh /endkind/getPaperMC.sh
COPY docker-entrypoint.sh /endkind/docker-entrypoint.sh

RUN chmod +x /endkind/getPaperMC.sh
RUN chmod +x /endkind/docker-entrypoint.sh

ARG PAPERMC_VERSION=1.19.4
RUN echo "$PAPERMC_VERSION" > /endkind/papermc_version

WORKDIR /papermc

VOLUME /papermc

ENV MIN_RAM=512M
ENV MAX_RAM=1G
ENV MINECRAFT_EULA=false
ENV JAVA_FLAGS="--add-modules=jdk.incubator.vector -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20"
ENV PAPERMC_FLAGS="--nojline"

ENTRYPOINT ["/endkind/docker-entrypoint.sh"]

