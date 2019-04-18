FROM python:3

COPY /core/ /epiphany
WORKDIR /epiphany/src/epicli

RUN mkdir /shared/

RUN pip install pipenv

RUN pipenv install --system --deploy

RUN chmod +x cli/epicli.py

ENV PYTHONPATH "${PYTHONPATH}:/epiphany/src/epicli"
ENV DOCKER_CLI Yes

WORKDIR /epiphany/src/epicli/cli

ENTRYPOINT ["/bin/bash"]
