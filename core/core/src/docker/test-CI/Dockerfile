FROM epiphanyregistry.azurecr.io/epiphany-deploy:latest

RUN mkdir /tmp/keys

RUN ssh-keygen -q -t rsa -m PEM -N '' -f /tmp/keys/id_rsa

RUN apk add --no-cache ruby ruby-rdoc ruby-irb ruby-rake ruby-etc

RUN gem install bundler -v 1.16.3

RUN bundle config --global silence_root_warning 1

WORKDIR /epiphany/core/core/test/serverspec

RUN bundle install

WORKDIR /epiphany

RUN chmod a+x /epiphany/core/core/src/docker/test-CI/run.sh

CMD ["/epiphany/core/core/src/docker/test-CI/run.sh"]
