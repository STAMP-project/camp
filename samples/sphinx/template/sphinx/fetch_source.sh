#!/usr/bin/env sh


SPHINX_REPOSITORY=https://github.com/sphinx-doc/sphinx.git
SPHINX_VERSION=v2.0.1

git clone --branch=${SPHINX_VERSION} ${SPHINX_REPOSITORY} src
mkdir -p src/camp
