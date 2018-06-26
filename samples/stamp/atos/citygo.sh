#!/bin/bash
# -*- ENCODING: UTF-8 -*-
#This script download CityGo app from Atos Repository
#
# Author: Fernando Mendez - fernando.mendez@atos.net
#

rm -rf ./repo
#Clone citygo from ARI gitlab
git clone https://gitlab.atosresearch.eu/ari/stamp_docker_citygoApp.git

#Copy required files to deploy citygo
mkdir ./repo
cp -R stamp_docker_citygoApp/repo/Showcase repo/
cp -R stamp_docker_citygoApp/repo/Postgres repo/
cp  stamp_docker_citygoApp/docker-compose-camp/docker-compose.yml docker-compose/

#Remove citygo ARI gitlab
rm -rf stamp_docker_citygoApp/




