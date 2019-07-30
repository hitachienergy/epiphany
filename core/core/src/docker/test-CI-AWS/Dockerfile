FROM epiphanyregistry.azurecr.io/epicli-deploy:latest

RUN mkdir /tmp/keys

RUN ssh-keygen -q -t rsa -m PEM -N '' -f /tmp/keys/id_rsa

RUN apk add --no-cache ruby ruby-rdoc ruby-irb ruby-rake ruby-etc

RUN gem install bundler -v 1.16.3

RUN bundle config --global silence_root_warning 1

RUN mkdir /serverspec

ADD core/test/serverspec/ /serverspec

WORKDIR /serverspec

RUN bundle install

WORKDIR /shared

ADD core/src/docker/test-CI-AWS/run.sh /shared

RUN chmod a+x /shared/run.sh

CMD ["/shared/run.sh"]
