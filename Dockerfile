# Pull base image
FROM python:3.6-alpine

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install packages
RUN apk add --update --no-cache --virtual .runtime-deps \
    jpeg-dev \
    gettext \
    nodejs \
    nodejs-npm

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt .
RUN apk add --no-cache --virtual .build-deps build-base git libxslt-dev zlib-dev postgresql-dev \
    && git config --global http.postBuffer 524288000 \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt --src /usr/local/src \
    && apk add --virtual .runtime-deps postgresql-client \
    && apk del .build-deps

COPY package.json .
RUN npm install
RUN npm install -g coffee-script@^1.12.6

# Copy project
COPY . /code/

# Entrypoint
ENTRYPOINT ["sh", "./docker-entrypoint.sh"]
