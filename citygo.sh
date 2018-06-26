#!/bin/bash
# -*- ENCODING: UTF-8 -*-
#This script download CityGo app from Atos Repository

rm -rf /repo
git clone https://gitlab.atosresearch.eu/ari/stamp_docker_citygoApp.git
cp -R stamp_docker_citygoApp/repo ./
rm -rf stamp_docker_citygoApp




