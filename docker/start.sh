#!/bin/bash

python ozepy/stamp/dockerbuild.py -d ./workingdir
cp ./workingdir/out/ampimages.yml ./workingdir/ampimages.yml
cp ./workingdir/out/genimages.yml ./workingdir/genimages.yml

python ozepy/stamp/dockercompose.py -d ./workingdir
cp ./workingdir/out/ampcompose.yml ./workingdir/ampcompose.yml

python conf-test-ampli/dockergen/src/dockerfilegen.py -i ./workingdir/genimages.yml
python conf-test-ampli/dockergen/src/composegen.py -i ./workingdir/ampcompose.yml
