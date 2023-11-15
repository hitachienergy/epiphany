FROM python:3.10.12-slim

ARG USERNAME=epiuser
ARG USER_UID=1000
ARG USER_GID=$USER_UID

ARG AWS_CLI_VERSION=2.0.30
ARG HELM_VERSION=3.3.1
ARG KUBECTL_VERSION=1.22.4
ARG KUBELOGIN_VERSION=0.0.33
ARG TERRAFORM_VERSION=1.1.3

ENV EPICLI_DOCKER_SHARED_DIR=/shared

COPY . /epicli

RUN : INSTALL APT REQUIREMENTS \
    && apt-get update \
    && apt-get install --no-install-recommends -y \
        autossh curl gcc git jq libcap2-bin libc6-dev libffi-dev make musl-dev openssh-client procps psmisc rsync ruby-full sudo tar unzip vim \
\
    && : INSTALL HELM BINARY \
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
\
    && : INSTALL AWS CLI BINARY \
    && curl -fsSLO https://awscli.amazonaws.com/awscli-exe-linux-x86_64-${AWS_CLI_VERSION}.zip \
    && unzip awscli-exe-linux-x86_64-${AWS_CLI_VERSION}.zip \
    && ./aws/install -i /usr/local/aws-cli -b /usr/local/bin \
    && rm -rf awscli-exe-linux-x86_64-${AWS_CLI_VERSION}.zip ./aws \
    && aws --version \
\
    && : INSTALL GEM REQUIREMENTS \
    && gem install net-ssh -v 6.1.0 \
    && gem install \
        bcrypt_pbkdf ed25519 rake rspec_junit_formatter serverspec \
\
    && : INSTALL PIP REQUIREMENTS \
    && pip install --disable-pip-version-check --no-cache-dir --default-timeout=100 \
        --requirement /epicli/.devcontainer/requirements.txt \
\
    && : INSTALLATION CLEANUP \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /epicli/.devcontainer/ \
\
    && : SETUP USER AND OTHERS \
    && groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && setcap 'cap_net_bind_service=+ep' /usr/bin/ssh \
\
    && : SETUP SHARED DIRECTORY \
    && mkdir -p $EPICLI_DOCKER_SHARED_DIR \
    && chown $USERNAME $EPICLI_DOCKER_SHARED_DIR \
    && chmod g+w $EPICLI_DOCKER_SHARED_DIR \
\
    && : SETUP EPICLI COMMAND \
    && mv /epicli/cli/epicli /bin/epicli \
    && chmod +x /bin/epicli

WORKDIR $EPICLI_DOCKER_SHARED_DIR

USER $USERNAME

ENTRYPOINT ["/bin/bash"]
