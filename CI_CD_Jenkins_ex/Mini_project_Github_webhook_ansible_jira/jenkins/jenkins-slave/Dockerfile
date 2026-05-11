FROM jenkins/inbound-agent:alpine

USER root

RUN apk add --no-cache -u libcurl curl bash

ARG DOCKER_VERSION=26.1.4
ARG DOCKER_COMPOSE_VERSION=2.27.1
ARG DOCKER_BUILDX_VERSION=0.16.0

RUN curl -fsSL https://download.docker.com/linux/static/stable/`uname -m`/docker-$DOCKER_VERSION.tgz | tar --strip-components=1 -xz -C /usr/local/bin docker/docker

RUN curl -fsSL https://github.com/docker/compose/releases/download/v$DOCKER_COMPOSE_VERSION/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose

RUN uname -m > /tmp/arch \
    && sed -i 's/x86_64/amd64/g' /tmp/arch \
    && mkdir -p /usr/libexec/docker/cli-plugins/ \
    && curl -fsSL https://github.com/docker/buildx/releases/download/v$DOCKER_BUILDX_VERSION/buildx-v$DOCKER_BUILDX_VERSION.linux-`cat /tmp/arch` > /usr/libexec/docker/cli-plugins/docker-buildx \
    && chmod +x /usr/libexec/docker/cli-plugins/docker-buildx \
    && docker buildx install \
    && rm /tmp/arch

# GITHUB CLI FOR WEBHOOKS 
ARG GH_VERSION=2.33.0
RUN curl -LO https://github.com/cli/cli/releases/download/v$GH_VERSION/gh_${GH_VERSION}_linux_amd64.tar.gz \
    && tar -xvf gh_${GH_VERSION}_linux_amd64.tar.gz \
    && mv gh_${GH_VERSION}_linux_amd64/bin/gh /usr/local/bin/ \
    && chmod +x /usr/local/bin/gh \
    && rm -rf gh_${GH_VERSION}_linux_amd64 gh_${GH_VERSION}_linux_amd64.tar.gz

USER jenkins