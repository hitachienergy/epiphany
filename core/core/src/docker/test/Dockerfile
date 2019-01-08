FROM openjdk:8-alpine

ENV SONARQUBE_SCANNER_VERSION 3.2.0.1227

ENV BUILD_PACKAGES \
  bash \
  unzip \
  wget \
  python \
  py-pip 

ENV BUILD_DEPENDENCIES \
  gcc \
  musl-dev \
  libffi-dev \
  openssl-dev \
  python-dev

RUN apk add build-base

RUN set -x && \
    \
    echo "==> Adding build-dependencies..."  && \
    apk --update add --virtual build-dependencies ${BUILD_DEPENDENCIES} && \
    \
    echo "==> Upgrading apk and system..."  && \
    apk update && apk upgrade && \
    \
    echo "==> Adding Python runtime..."  && \
    apk add --no-cache ${BUILD_PACKAGES} && \
    pip install --upgrade pip && \
    \
    echo "==> Installing linters..."  && \
    pip install ansible-lint pylint && \
    \
    echo "==> Installing Sonar-scanner..."  && \
    mkdir -p /opt && \
    wget -q -O /sonar-scanner-cli.zip "http://central.maven.org/maven2/org/sonarsource/scanner/cli/sonar-scanner-cli/${SONARQUBE_SCANNER_VERSION}/sonar-scanner-cli-${SONARQUBE_SCANNER_VERSION}.zip" && \
    unzip /sonar-scanner-cli.zip -d /opt && \
    \
    echo "==> Cleaning up..."  && \
    apk del build-dependencies && \
    apk del --purge wget unzip && \     
    rm -rf /var/cache/apk/* /sonar-scanner-cli.zip

ENV SONAR_RUNNER_HOME=/opt/sonar-scanner-${SONARQUBE_SCANNER_VERSION}
ENV PATH $PATH:$SONAR_RUNNER_HOME/bin

RUN mkdir /epiphany/
WORKDIR /epiphany/
ADD . /epiphany/
RUN chmod +x /epiphany/core/src/docker/test/run.sh

ENTRYPOINT ["/epiphany/core/src/docker/test/run.sh"]
