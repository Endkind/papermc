FROM eclipse-temurin:11
RUN apt-get update && apt-get install -y \
    curl \
    jq

LABEL Author Endkind Ender <endkind.ender@endkind.net>

COPY getPaperMC.sh /endkind/getPaperMC.sh
COPY docker-entrypoint.sh /endkind/docker-entrypoint.sh

RUN chmod +x /endkind/getPaperMC.sh
RUN chmod +x /endkind/docker-entrypoint.sh

ARG PAPERMC_VERSION=1.14.4
RUN echo "$PAPERMC_VERSION" > /endkind/papermc_version

WORKDIR /papermc

VOLUME /papermc

ENV MIN_RAM=512M
ENV MAX_RAM=1G
ENV PAPERMC_FLAGS="--nojline"

ENTRYPOINT ["/endkind/docker-entrypoint.sh"]

