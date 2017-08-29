#!/bin/bash

IMAGE=vassik/config-testing:latest
APP=config-testing

docker stop $APP
docker rm $APP
docker rmi -f $IMAGE
docker build --rm -t $IMAGE .
docker run -d -v /var/run/docker.sock:/var/run/docker.sock -e MASTER_SSH_PORT=22 -e MASTER_SLAVE_USER=jenkins -e MASTER_SLAVE_PWD=jenkins -e DOCKER_GID=998 --name $APP $IMAGE
#docker exec -it $APP bash -c "su - jenkins"
docker exec -it $APP bash
