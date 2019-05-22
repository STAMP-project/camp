#!/usr/bin/env sh

PURESCRIPT_VERSION=0.12.5

mkdir purescript/src
cd purescript/src
git clone https://github.com/purescript/purescript.git . && git checkout v$PURESCRIPT_VERSION

#copy a modified package.yaml, which allows using specific version numbers for depedencies
rm -f package.yaml
cp ../package.yaml package.yaml
