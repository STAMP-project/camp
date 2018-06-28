#!/bin/bash
# -*- ENCODING: UTF-8 -*-
#This script download CityGo app from Atos Repository and start CAMP 
#
# Author: Fernando Mendez - fernando.mendez@atos.net

rm -rf ./repo
rm -rf ./docker-compose

#Clone citygo repo from ARI gitlab
git clone https://gitlab.atosresearch.eu/ari/stamp_docker_citygoApp.git

#Copy required files to deploy citygo APP
echo "Copy requiered files to deploy citygo APP"
mkdir ./repo
cp -R stamp_docker_citygoApp/repo/Showcase repo/
cp -R stamp_docker_citygoApp/repo/Postgres repo/
mkdir ./docker-compose
cp stamp_docker_citygoApp/docker-compose-camp/docker-compose.yml docker-compose/

#Start CAMP and build dockerfiles images
echo "Starting Camp tool"
cd ../../../../camp/docker && docker build -t camp-tool:latest .
echo "Building Camp dockerfiles"
cd /samples/stamp/atos/ && docker run -it -v $(pwd):/root/workingdir songhui/camp /bin/bash allinone.sh
docker build repo/Showcase/ -t showcase:python2.7
docker build repo/Postgres/ -t postgres:ubuntu-latest

#Copy Stress Test script
echo "Creating tests stress..."
mkdir ./Tests
cp -R stamp_docker_citygoApp/Tests/version2/Test-version2.jmx Tests/
cp -R stamp_docker_citygoApp/Tests/version2/executeCamp.sh Tests/
cp -R stamp_docker_citygoApp/Tests/version2/Result.jtl Tests/

#Remove citygo repo
rm -rf stamp_docker_citygoApp/

echo "Deploying citygo from compose1 folder"
echo "-------------------------------------"
cd ./compose1
docker-compose up -d

echo "Executing stress Test to CityGo Backend"
echo "---------------------------------------"
cd ./Tests
./executeCamp.sh
