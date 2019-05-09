#!/usr/bin/env sh

#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#

# Setup all the dependencies needed to test Ruby on rails. See the
# documentation at:
# https://edgeguides.rubyonrails.org/development_dependencies_install.html

set -o errexit
set -o errtrace
set -o pipefail
set -o nounset

apt-get update
apt-get install -y --no-install-recommends \
        emacs-nox \
        git \
        build-essential \
        libmariadbclient-dev \
        libxml2-dev \
        libpq-dev \
        libncurses5-dev libncursesw5-dev \
        sqlite3 libsqlite3-dev \
        redis-server \
        memcached \
        mysql-server \
        postgresql postgresql-contrib \
        ffmpeg \
        mupdf mupdf-tools

# Install Ruby dependencies, needed for later creating the test DBs
bundle install

# Install YARN through APT failed.
# $ apt-get install -y --no-install-recommends yarn

# Install YARN manually, did not work
# $ apt-get remove -y cmdtest
# $ apt-get remove -y yarn
# $ curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
# $ echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
# $ apt-get install -y --no-install-recommends  yarn

# Install Javascript environment:
# 1. Installing NodeJS (shipped with NPM)
# 2. Use NPM to install YARN
apt-get install -y --no-install-recommends curl software-properties-common
curl -sL https://deb.nodesource.com/setup_10.x | bash -
apt-get install -y  nodejs
npm install yarn -g

# Install Javascript dependencies (using yarn)
yarn install

# Cleanup
apt-get clean
rm -rf /var/lib/apt/lists/*


