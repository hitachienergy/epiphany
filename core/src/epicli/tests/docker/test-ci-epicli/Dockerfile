ARG BUILD_ID

FROM epicli:$BUILD_ID

RUN sudo apt-get update \
&& sudo apt-get -y install ruby-full \
&& sudo gem install serverspec rake rspec_junit_formatter

RUN ssh-keygen -q -t rsa -m PEM -N '' -f ~/.ssh/id_rsa

COPY tests/serverspec-cli/ /serverspec

WORKDIR /serverspec

ENTRYPOINT ["/bin/bash"]
