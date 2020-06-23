FROM python:3.7-slim

ARG EPICLI_VERSION

ARG USERNAME=epiuser
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG SHARED_DIR=/shared

ENV DOCKER_CLI Yes

COPY /dist/ /epicli
WORKDIR /epicli

RUN apt-get update \
    && apt-get -y install gcc make musl-dev libffi-dev tar unzip openssh-client vim \
    && apt-get -y install ruby-full \
    && gem install serverspec rake rspec_junit_formatter

RUN pip install epicli-${EPICLI_VERSION}-py3-none-any.whl

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir $SHARED_DIR \
    ;chown :$USERNAME $SHARED_DIR \
    && chmod g+w $SHARED_DIR

WORKDIR $SHARED_DIR

USER $USERNAME

ENTRYPOINT ["/bin/bash"]