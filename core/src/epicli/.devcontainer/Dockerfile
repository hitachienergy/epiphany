FROM python:3.7-slim

ENV DEBIAN_FRONTEND=noninteractive

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

COPY cert/cert.md cert/*.crt /usr/local/share/ca-certificates/
COPY cert/cert.md cert/*.pem /
COPY cert/config-pre.sh /
COPY cert/config-post.sh /
COPY requirements.txt /

RUN chmod +x /config-pre.sh \
    && /bin/bash -c /config-pre.sh \

    && apt-get update \
    && apt-get -y install --no-install-recommends apt-utils dialog 2>&1 \

    && apt-get -y install git git-lfs procps lsb-release gcc make musl-dev libffi-dev tar unzip vim \

    && apt-get -y install ruby-full \

    && gem install serverspec rake rspec_junit_formatter \

    && pip --disable-pip-version-check --no-cache-dir install -r /requirements.txt --default-timeout=100 \

    && pip --disable-pip-version-check --no-cache-dir install pipenv pylint pytest wheel setuptools twine --default-timeout=100 \

    && groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \

    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \

    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/* \

    && chmod +x /config-post.sh \
    && /bin/bash -c /config-post.sh

ENV DEBIAN_FRONTEND=
