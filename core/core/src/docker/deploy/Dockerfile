FROM epiphanyplatform/epiphany-dev:latest

RUN mkdir /epiphany/core/ \
    && mkdir /epiphany/core/data/ \
    && mkdir /epiphany/core/build/

ADD ./core/ /epiphany/core/    

CMD ["/epiphany/core/core/src/docker/deploy/init.sh"]
