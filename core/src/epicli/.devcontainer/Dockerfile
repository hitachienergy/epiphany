FROM python:3.7-slim

ARG HELM_VERSION=3.3.1
ARG KUBECTL_VERSION=1.18.8

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
        autossh curl gcc jq libcap2-bin libffi-dev make musl-dev openssh-client procps psmisc ruby-full sudo tar unzip vim \
        \
        git git-lfs lsb-release \
\
    && echo "Installing helm binary ..." \
    && curl -fsSLO https://get.helm.sh/helm-v${HELM_VERSION}-linux-amd64.tar.gz \
    && tar -xzof ./helm-v${HELM_VERSION}-linux-amd64.tar.gz --strip=1 -C /usr/local/bin linux-amd64/helm \
    && rm ./helm-v${HELM_VERSION}-linux-amd64.tar.gz \
    && helm version \
    && echo "Installing kubectl binary ..." \
    && curl -fsSLO https://storage.googleapis.com/kubernetes-release/release/v${KUBECTL_VERSION}/bin/linux/amd64/kubectl \
    && chmod +x ./kubectl \
    && mv ./kubectl /usr/local/bin/kubectl \
    && kubectl version --client \
\
    && setcap 'cap_net_bind_service=+ep' /usr/bin/ssh \
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
