FROM python:3.11.7-alpine

WORKDIR /app

COPY . /app

# install dependencies
RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && pip install --no-cache-dir -r ./requirements.txt \
    && apk del .build-deps

