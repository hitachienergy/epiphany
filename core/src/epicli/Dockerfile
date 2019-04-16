FROM python:3

COPY /core/ /epiphany
WORKDIR /epiphany/src/epicli

RUN mkdir /epiphany/src/epicli/input/ \
    && mkdir /epiphany/src/epicli/output/

RUN pip install pipenv

RUN pipenv install --system --deploy

RUN chmod +x cli/epicli.py

ENV PYTHONPATH "${PYTHONPATH}:/epiphany/src/epicli"

WORKDIR /epiphany/src/epicli/cli

ENTRYPOINT ["/bin/bash"]
