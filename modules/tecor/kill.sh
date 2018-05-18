#!/bin/bash

IMAGE=vassik/config-testing:latest
APP=config-testing

docker stop $APP
docker rm $APP
docker rmi -f $IMAGE