FROM python:3.7-slim

ARG HELM_VERSION=3.3.0*
ARG KUBECTL_VERSION=1.18.8*

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
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get install --no-install-recommends -y \
        apt-utils dialog 2>&1 \
    && apt-get install --no-install-recommends -y \
        curl gcc gnupg2 libffi-dev make musl-dev openssh-client ruby-full sudo tar unzip vim \
        \
        git git-lfs lsb-release procps \
\
    && echo "Adding APT repositories ..." \
    && curl -s https://baltocdn.com/helm/signing.asc | APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1 apt-key add - \
    && echo "deb https://baltocdn.com/helm/stable/debian/ all main" | tee /etc/apt/sources.list.d/helm-stable-debian.list \
    && curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1 apt-key add - \
    && echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | tee /etc/apt/sources.list.d/kubernetes.list \
    && apt-get update \
    && apt-get install --no-install-recommends -y \
        helm=${HELM_VERSION} \
        kubectl=${KUBECTL_VERSION} \
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
