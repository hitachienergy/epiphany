FROM python:3.7

COPY . /app
WORKDIR /app

RUN pip install pipenv

RUN pipenv install --system --deploy

CMD ["python", "main.py"]