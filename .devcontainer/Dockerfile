FROM python:3.10.13-slim

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

ARG AWS_CLI_VERSION=2.0.30
ARG HELM_VERSION=3.3.1
ARG KUBECTL_VERSION=1.22.4
ARG KUBELOGIN_VERSION=0.0.33
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
    openjdk-17-jre-headless \
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
 && : INSTALL KUBELOGIN BINARY \
 && curl -fsSLO https://github.com/Azure/kubelogin/releases/download/v${KUBELOGIN_VERSION}/kubelogin-linux-amd64.zip \
 && unzip -j kubelogin-linux-amd64.zip -d /usr/local/bin \
 && rm kubelogin-linux-amd64.zip \
 && kubelogin --version \
 && : INSTALL TERRAFORM BINARY \
 && curl -fsSLO https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
 && unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip -d /usr/local/bin \
 && rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
 && terraform version \
 && : INSTALL AWS CLI BINARY \
 && curl -fsSLO https://awscli.amazonaws.com/awscli-exe-linux-x86_64-${AWS_CLI_VERSION}.zip \
 && unzip awscli-exe-linux-x86_64-${AWS_CLI_VERSION}.zip \
 && ./aws/install -i /usr/local/aws-cli -b /usr/local/bin \
 && rm -rf awscli-exe-linux-x86_64-${AWS_CLI_VERSION}.zip ./aws \
 && aws --version

RUN : INSTALL GEM REQUIREMENTS \
 && gem install net-ssh -v 6.1.0 \
 && gem install \
    bcrypt_pbkdf ed25519 rake rspec_junit_formatter rubocop rubocop-junit_formatter serverspec solargraph

COPY requirements.txt /

RUN : INSTALL PIP REQUIREMENTS \
 && pip install --disable-pip-version-check --no-cache-dir --default-timeout=100 \
    --requirement /requirements.txt \
 && pip install --disable-pip-version-check --no-cache-dir --default-timeout=100 \
    poetry pylint==2.* pylint_junit ansible-lint==6.5.0 ansible-lint-to-junit-xml yamllint pytest pytest_mock setuptools twine wheel

RUN : SETUP USER AND OTHERS \
 && groupadd --gid $USER_GID $USERNAME \
 && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
 && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
 && chmod ug=r,o= /etc/sudoers.d/$USERNAME \
 && setcap 'cap_net_bind_service=+ep' /usr/bin/ssh

RUN : SETUP JAVE_HOME
ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk-amd64/

RUN : SETUP EPICLI ALIAS \
 && echo alias epicli='"export PYTHONPATH=/workspaces/epiphany && python3 -m cli.epicli"' >> /etc/bash.bashrc
