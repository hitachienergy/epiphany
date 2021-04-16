FROM alpine:3.12.0

RUN apk add --update --no-cache make=4.3-r0 curl &&\
    wget $(curl -s https://api.github.com/repos/mikefarah/yq/releases/latest | grep browser_download_url | grep linux_amd64 | cut -d '"' -f 4) -O /usr/bin/yq &&\
    chmod +x /usr/bin/yq

ENV C_WORKDIR "/workdir"
ENV C_TEMPLATES "/mocks"
ENV C_SHARED "/shared"
ENV C_CONFIG "azi-config.yml"

WORKDIR /workdir
ENTRYPOINT ["make"]

COPY mocks /mocks
COPY workdir /workdir
