ARG BUILD_ID

FROM epicli:$BUILD_ID

RUN sudo apt-get update \
&& sudo apt-get -y install ruby-full \
&& sudo gem install serverspec rake rspec_junit_formatter

COPY --chown=epiuser:epiuser tests/serverspec-cli/ /serverspec
