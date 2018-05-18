#!/bin/bash

APP_NAME=tecor-demo
IMAGE_NAME=vassik/tecor-demo:latest
docker stop $APP_NAME
docker rm $APP_NAME
docker rmi $IMAGE_NAME
docker run -dit -p 8071:80 --name $APP_NAME $IMAGE_NAME