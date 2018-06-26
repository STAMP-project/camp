#!/bin/bash
# -*- ENCODING: UTF-8 -*-
#This script download CityGo app from Atos Repository and start CAMP 
#
# Author: Fernando Mendez - fernando.mendez@atos.net

rm -rf ./repo
#Clone citygo repo from ARI gitlab
git clone https://gitlab.atosresearch.eu/ari/stamp_docker_citygoApp.git

#Copy required files to deploy citygo APP
mkdir ./repo
cp -R stamp_docker_citygoApp/repo/Showcase repo/
cp -R stamp_docker_citygoApp/repo/Postgres repo/
cp  stamp_docker_citygoApp/docker-compose-camp/docker-compose.yml docker-compose/

#Remove citygo repo
rm -rf stamp_docker_citygoApp/

#Start CAMP and build dockerfiles images
docker run -it -v $(pwd):/root/workingdir songhui/camp /bin/bash allinone.sh
docker build repo/Showcase/ -t showcase:python2.7
docker build repo/Postgres/ -t postgres:ubuntu-latest

echo "Deploying citygo from compose1 folder"
echo "--------------------------------------"
cd ./compose1
docker-compose up -d

