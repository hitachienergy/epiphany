FROM python:3.10-slim

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

ARG HELM_VERSION=3.3.1
ARG KUBECTL_VERSION=1.22.4
ARG TERRAFORM_VERSION=1.1.3

RUN : INSTALL APT REQUIREMENTS \
 && export DEBIAN_FRONTEND=noninteractive \
 && apt-get -q update \
 && apt-get -q install -y --no-install-recommends \
    apt-utils dialog \
 && apt-get -q install -y --no-install-recommends \
    autossh curl gcc git git-lfs iputils-ping \
    jq libc6-dev libcap2-bin libffi-dev lsb-release \
    make musl-dev openssh-client procps \
    psmisc rsync ruby-full sudo tar \
    unzip vim \
 && apt-get -q autoremove -y \
 && apt-get -q clean -y \
 && rm -rf /var/lib/apt/lists/*

RUN : INSTALL HELM BINARY \
 && curl -fsSLO https://get.helm.sh/helm-v${HELM_VERSION}-linux-amd64.tar.gz \
 && tar -xzof ./helm-v${HELM_VERSION}-linux-amd64.tar.gz --strip=1 -C /usr/local/bin linux-amd64/helm \
 && rm ./helm-v${HELM_VERSION}-linux-amd64.tar.gz \
 && helm version \
 && : INSTALL KUBECTL BINARY \
 && curl -fsSLO https://storage.googleapis.com/kubernetes-release/release/v${KUBECTL_VERSION}/bin/linux/amd64/kubectl \
 && chmod +x ./kubectl \
 && mv ./kubectl /usr/local/bin/kubectl \
 && kubectl version --client \
 && : INSTALL TERRAFORM BINARY \
 && curl -fsSLO https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
 && unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip -d /usr/local/bin \
 && rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
 && terraform version

RUN : INSTALL GEM REQUIREMENTS \
 && gem install \
    bcrypt_pbkdf ed25519 rake rspec_junit_formatter rubocop rubocop-junit_formatter serverspec solargraph

COPY requirements.txt /

RUN : INSTALL PIP REQUIREMENTS \
 && pip install --disable-pip-version-check --no-cache-dir --default-timeout=100 \
    --requirement /requirements.txt \
 && pip install --disable-pip-version-check --no-cache-dir --default-timeout=100 \
    poetry pylint pylint_junit ansible-lint ansible-lint-to-junit-xml yamllint pytest pytest_mock setuptools twine wheel

RUN : SETUP USER AND OTHERS \
 && groupadd --gid $USER_GID $USERNAME \
 && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
 && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
 && chmod ug=r,o= /etc/sudoers.d/$USERNAME \
 && setcap 'cap_net_bind_service=+ep' /usr/bin/ssh

RUN : SETUP EPICLI ALIAS \
 && echo alias epicli='"export PYTHONPATH=/workspaces/epiphany && python3 -m cli.epicli"' >> /etc/bash.bashrc
