#!/bin/bash

IMAGE=vassik/config-testing:latest
APP=config-testing
SHARED=/tmp/testing_report
SUT=xwiki-platform-vassik

if [[ -n $1 ]]; then
    DOCKERGID=$1
else
    DOCKERGID=998
fi

echo "copying SUT"
rm -rf ./$SUT
cp -R ../$SUT .

rm -rf $HOME/$SHARED
docker stop $APP
docker rm $APP
docker rmi -f $IMAGE
docker build --rm -t $IMAGE .
#docker run -i -v /var/run/docker.sock:/var/run/docker.sock -v $HOME/$SHARED:/var/jenkins_home -e MASTER_SSH_PORT=22 -e MASTER_SLAVE_USER=jenkins -e MASTER_SLAVE_PWD=jenkins -e DOCKER_GID=998 --name $APP $IMAGE
docker run -v /var/run/docker.sock:/var/run/docker.sock -v $HOME/$SHARED:/var/jenkins_home/report/ -e MASTER_SSH_PORT=22 -e MASTER_SLAVE_USER=jenkins -e MASTER_SLAVE_PWD=jenkins -e DOCKER_GID=$DOCKERGID --name $APP $IMAGE
#docker run -d -v /var/run/docker.sock:/var/run/docker.sock -e MASTER_SSH_PORT=22 -e MASTER_SLAVE_USER=jenkins -e MASTER_SLAVE_PWD=jenkins -e DOCKER_GID=998 --name $APP $IMAGE
#docker exec -it $APP bash -c "su - jenkins"
#docker exec -it $APP bash