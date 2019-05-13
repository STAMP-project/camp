#!/usr/bin/env bash

BASEDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd out
for d in */ ; do
    echo $d
    cd $BASEDIR/out/$d/images/atom_0
    (docker build -t bmorin/atom-${d::-1} .) 2>&1 | tee ../../test.log
    docker rmi -f bmorin/atom-${d::-1}
    sed -n -e '/passing/,$p' ../../test.log > ../../test_results.log
done
