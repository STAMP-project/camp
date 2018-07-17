#!/bin/bash

rm -rf ./workingdir/build
rm -rf ./workingdir/out
rm -f ./workingdir/ampimages.yml
rm -f ./workingdir/genimages.yml
rm -f ./workingdir/ampcompose.yml
mkdir ./workingdir/build
mkdir ./workingdir/out

START=$(date +%s.%N)

python ozepy/stamp/dockerbuild.py -d ./workingdir
cp ./workingdir/out/ampimages.yml ./workingdir/ampimages.yml
cp ./workingdir/out/genimages.yml ./workingdir/genimages.yml

if [ -f ./workingdir/composite.yml ]
then
    python ozepy/stamp/dockercompose.py -d ./workingdir
    cp ./workingdir/out/ampcompose.yml ./workingdir/ampcompose.yml
fi

python camp/src/dockerfilegen.py -i ./workingdir/genimages.yml

if [ -f ./workingdir/composite.yml ]
then
    python camp/src/composegen.py -i ./workingdir/ampcompose.yml
fi

if [ -f ./workingdir/resolmodel.yml ]
then
    cp ./working/out/ampcompose.yml ./workingdir/ampcompose.yml
    #python camp-realize/camp_real_engine/rcamp.py -i workingdir/resolmodel.yml
    if [ -x "$(command -v rcamp)" ]; then
    	rcamp realize ./workingdir/resolmodel.yml
    else
    	echo "rcamp is not installed, variables will not be materialized"
    fi 
fi

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)
echo "Generated in $DIFF sec" 
chmod -R a+rw . 

echo ""
echo "===========Searching finished.========="
echo "Build all the generated images by: cd <your_dir>/build && bash ./build.sh"
echo "Launch one of the configurations by: docker-compose <your_dir>/docker-compose/docker-comopose-<number>.yml up"
