FROM python:3.6-alpine

ENV PATH="$PATH:/bin/bash"
ENV PYTHONPATHP "/"
ENV PYTHONUNBUFFERED 1
ENV DJANGO_DB_PASS "secret"
ENV BASE_STATISTICS_DB_PASS "secret"

COPY . /app
WORKDIR /app

# Installing client libraries and any other package you need
RUN apk update && apk add libpq

# Installing build dependencies
RUN apk add --virtual .build-deps gcc python-dev musl-dev postgresql-dev
RUN pip  install -r requirements.txt

RUN apk add bash

