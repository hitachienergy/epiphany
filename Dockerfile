# === Build epicli wheel file ===

FROM python:3.7-slim AS build-epicli-wheel

COPY . /src
WORKDIR /src/core/src/epicli

RUN python setup.py bdist_wheel

# === Build final image ===

FROM python:3.7-slim

ARG USERNAME=epiuser
ARG USER_UID=1000
ARG USER_GID=$USER_UID

ENV EPICLI_DOCKER_SHARED_DIR=/shared

COPY --from=build-epicli-wheel /src/core/src/epicli/dist/ /epicli/

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        gcc libffi-dev make musl-dev openssh-client ruby-full sudo tar unzip vim \
    && gem install \
        rake rspec_junit_formatter serverspec \
    && pip install --disable-pip-version-check --no-cache-dir \
        /epicli/epicli-*-py3-none-any.whl \
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
    && mkdir -p $EPICLI_DOCKER_SHARED_DIR \
    && chown $USERNAME $EPICLI_DOCKER_SHARED_DIR \
    && chmod g+w $EPICLI_DOCKER_SHARED_DIR

WORKDIR $EPICLI_DOCKER_SHARED_DIR

USER $USERNAME

ENTRYPOINT ["/bin/bash"]
