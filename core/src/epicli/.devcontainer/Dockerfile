FROM python:3.7

ENV DEBIAN_FRONTEND=noninteractive

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN apt-get update \
    && apt-get -y install --no-install-recommends apt-utils dialog 2>&1 \

    && apt-get -y install git procps lsb-release gcc make musl-dev libffi-dev tar unzip \

    && apt-get -y install ruby-full \

    && gem install serverspec rake rspec_junit_formatter \

    && pip --disable-pip-version-check --no-cache-dir install pylint \

    && pip --disable-pip-version-check --no-cache-dir install pipenv \

    && groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \

    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \

    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

ENV DEBIAN_FRONTEND=


