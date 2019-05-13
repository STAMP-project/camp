#!/usr/bin/env bash

BASEDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd out
for d in */ ; do
    echo $d
    cd $BASEDIR/out/$d/images/purescript_0

    #See https://github.com/STAMP-project/camp/issues/57
    sed -i '/stability: experimental/Q' src/package.yaml

    (docker build -t bmorin/purescript-${d::-1} .) 2>&1 | tee ../../test.log
    docker rm -f $(docker ps -aq)
    docker rmi -f bmorin/purescript-${d::-1}
    sed -n -e '/passed/,$p' ../../test.log > ../../test_results.log
done
