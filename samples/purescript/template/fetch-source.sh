#!/usr/bin/env sh

PURESCRIPT_VERSION=0.12.5

mkdir purescript/src || cd purescript/src && git clone https://github.com/purescript/purescript.git . && git checkout v$PURESCRIPT_VERSION
