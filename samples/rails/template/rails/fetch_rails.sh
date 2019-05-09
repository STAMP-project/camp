#!/usr/bin/env sh


RAILS_REPOSITORY=https://github.com/rails/rails.git
RAILS_VERSION=v5.2.3

git clone --branch=${RAILS_VERSION} ${RAILS_REPOSITORY} rails

# Activate the generation of JUnit XML test reports
sed -i "/group :test do/a \ \ gem \"minitest-ci\"" rails/Gemfile
