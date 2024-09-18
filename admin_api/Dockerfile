FROM python:3.11.7-alpine

WORKDIR /app

COPY . /app

# install dependencies
RUN apk add --virtual .build-deps gcc musl-dev \
    && pip install -r ./requirements.txt \
    && apk del .build-deps

