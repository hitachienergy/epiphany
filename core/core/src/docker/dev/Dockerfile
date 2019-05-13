FROM alpine:3.9.3

ENV TERRAFORM_VERSION 0.11.9
ENV ANSIBLE_VERSION 2.7

RUN apk add --update wget ca-certificates unzip git bash && \
    wget -q -O /terraform.zip "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip" && \
    unzip /terraform.zip -d /bin && \
    apk del --purge wget ca-certificates unzip && \
    rm -rf /var/cache/apk/* /terraform.zip

ENV BUILD_PACKAGES \
  bash \
  curl \
  tar \
  openssh-client \
  sshpass \
  git \
  python \
  py-boto \
  py-dateutil \
  py-httplib2 \
  py-jinja2 \
  py-paramiko \
  py-pip \
  ca-certificates \
  jq

RUN apk add build-base

RUN set -x && \
    \
    echo "==> Adding build-dependencies..."  && \
    apk --update add --virtual build-dependencies \
      gcc \
      musl-dev \
      libffi-dev \
      openssl-dev \
      python-dev && \
    \
    echo "==> Upgrading apk and system..."  && \
    apk update && apk upgrade && \
    \
    echo "==> Adding Python runtime..."  && \
    apk add --no-cache ${BUILD_PACKAGES} && \
    pip install --upgrade pip && \
    pip install python-keyczar docker-py && \
    \
    echo "==> Installing Ansible..."  && \
    pip install ansible==${ANSIBLE_VERSION} && \
    \
    echo "==> installing azure-cli..." && \
    pip install azure-cli && \
    # Uninstall pyOpenSSL: https://github.com/erjosito/ansible-azure-lab/issues/5
    echo "==> un-installing pyOpenSSL... " && \
    pip uninstall -y pyOpenSSL && \    
    \
    echo "==> Cleaning up..."  && \
    apk del build-dependencies && \
    rm -rf /var/cache/apk/* && \
    \
    echo "==> Adding hosts for convenience..."  && \
    mkdir -p /etc/ansible /ansible && \
    echo "[local]" >> /etc/ansible/hosts && \
    echo "localhost" >> /etc/ansible/hosts

ENV ANSIBLE_GATHERING smart \
  ANSIBLE_HOST_KEY_CHECKING false \
  ANSIBLE_RETRY_FILES_ENABLED false \
  ANSIBLE_ROLES_PATH /ansible/playbooks/roles \
  ANSIBLE_SSH_PIPELINING True \
  PYTHONPATH /ansible/lib \
  PATH /ansible/bin:$PATH \
  ANSIBLE_LIBRARY /ansible/library

RUN mkdir /epiphany/
WORKDIR /epiphany/

RUN terraform --version
RUN python --version
RUN ansible --version
RUN az --version

ENTRYPOINT ["/bin/bash"]
