#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


FROM ruby:2.6.3-stretch
# PostgreSQL installation fails on ruby:2.6.3-slim-stretch


LABEL maintainer "franck.chauvel@sintef.no"

RUN apt-get update && \
        apt-get install -y --no-install-recommends \
        git \
#        systemd systemd-sysv\
        build-essential \
        libmariadbclient-dev \
        libxml2-dev \
        libpq-dev \
        libncurses5-dev libncursesw5-dev \
        sqlite3 libsqlite3-dev \
        redis-server \
        memcached \
        mysql-server \
        nodejs \
        postgresql postgresql-contrib \
        && \
        apt-get clean && \
        rm -rf /var/lib/apt/lists/*

# Start the MySQL service
RUN service mysql start

# Start the PostgreSQL service
RUN service postgresql start

# Start the redis server
RUN service redis-server start

# Start the memcached service
RUN service memcached start

COPY rails /opt/rails

WORKDIR /opt/rails

RUN bundle install

#RUN bundle exec rake test
