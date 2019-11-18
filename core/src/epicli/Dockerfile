FROM python:3.7-alpine

ARG EPICLI_VERSION

ENV DOCKER_CLI Yes

COPY /dist/ /epicli
WORKDIR /epicli

RUN apk -U add gcc make musl-dev libffi-dev openssl-dev bash openssh tar unzip

RUN pip install epicli-${EPICLI_VERSION}-py3-none-any.whl

RUN mkdir /shared/
WORKDIR /shared

ENTRYPOINT ["/bin/bash"]
