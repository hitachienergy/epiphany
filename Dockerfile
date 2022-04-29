FROM python:3.10-slim

ARG USERNAME=epiuser
ARG USER_UID=1000
ARG USER_GID=$USER_UID

ARG HELM_VERSION=3.3.1
ARG KUBECTL_VERSION=1.22.4
ARG TERRAFORM_VERSION=1.1.3

ENV EPICLI_DOCKER_SHARED_DIR=/shared

COPY . /epicli

RUN : INSTALL APT REQUIREMENTS \
    && apt-get update \
    && apt-get install --no-install-recommends -y \
        autossh curl gcc jq libcap2-bin libc6-dev libffi-dev make musl-dev openssh-client procps psmisc rsync ruby-full sudo tar unzip vim \
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
    && : INSTALL TERRAFORM BINARY \
    && curl -fsSLO https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
    && unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip -d /usr/local/bin \
    && rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
    && terraform version \
\
    && : INSTALL GEM REQUIREMENTS \
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
