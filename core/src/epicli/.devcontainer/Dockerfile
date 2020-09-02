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
\
    && apt-get update \
    && apt-get install --no-install-recommends -y \
        apt-utils dialog 2>&1 \
    && apt-get install --no-install-recommends -y \
        gcc libffi-dev make musl-dev openssh-client ruby-full sudo tar unzip vim \
        \
        git git-lfs lsb-release procps \
\
    && gem install \
        rake rspec_junit_formatter serverspec \
\
    && pip install --disable-pip-version-check --no-cache-dir --default-timeout=100 \
        --requirement /requirements.txt \
    && pip install --disable-pip-version-check --no-cache-dir --default-timeout=100 \
        pipenv pylint pytest setuptools twine wheel \
\
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/* \
\
    && groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
\
    && chmod +x /config-post.sh \
    && /bin/bash -c /config-post.sh

ENV DEBIAN_FRONTEND=
