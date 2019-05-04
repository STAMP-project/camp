#!/usr/bin/env sh

ATOM_VERSION=1.36.1


curl --silent -O -J -L https://github.com/atom/atom/archive/v$ATOM_VERSION.zip
unzip -qq atom-$ATOM_VERSION.zip -d .
rm atom-$ATOM_VERSION.zip
mv atom-$ATOM_VERSION atom/src
