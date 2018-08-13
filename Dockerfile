FROM ruby:2.5.0-alpine3.7

RUN apk add --update \
  build-base \
  libxml2-dev \
  libxslt-dev \
  nodejs \
  git \
  xvfb \
  file \
  imagemagick \
  mariadb-dev \
  postgresql-dev && \
  rm -rf /var/cache/apk/*

WORKDIR /app

COPY package.json package.json
RUN npm install

COPY Gemfile Gemfile
COPY Gemfile.lock Gemfile.lock
RUN bundle install --jobs 20 --retry 5

COPY . /app
