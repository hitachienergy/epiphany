FROM epiphany-dev:latest

ADD ./core/ /epiphany/

RUN mkdir /epiphany/data/ \
    && mkdir /epiphany/build/

CMD ["/epiphany/core/src/docker/deploy/init.sh"]
