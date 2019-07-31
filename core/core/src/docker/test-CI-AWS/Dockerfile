FROM epiphanyregistry.azurecr.io/epicli:latest

RUN mkdir /tmp/keys

RUN ssh-keygen -q -t rsa -m PEM -N '' -f /tmp/keys/id_rsa

RUN apk add --no-cache ruby ruby-rdoc ruby-irb ruby-rake ruby-etc

RUN gem install bundler -v 1.16.3

RUN bundle config --global silence_root_warning 1

RUN mkdir /serverspec

ADD core/test/serverspec/ /serverspec

WORKDIR /serverspec

RUN bundle install

ADD core/src/docker/test-CI-AWS/run.sh /tmp

RUN chmod a+x /tmp/run.sh

CMD ["/tmp/run.sh"]
