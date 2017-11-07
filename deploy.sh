#!/bin/bash

#IMAGE=vassik/config-testing:latest
#APP=config-testing
#SHARED=/tmp/testing_report
#SUT=bvr-diversity
#deploy.sh -g=998 -i=vassik/config-testing:latest -a=config-testing -s=/tmp/testing_report/ -t=bvr-diversity

for i in "$@"; do
    case $i in
        -g=*)
        DOCKERGID="${i#*=}"
        shift # past argument=value
        ;;
        -i=*)
        IMAGE="${i#*=}"
        shift # past argument=value
        ;;
        -a=*)
        APP="${i#*=}"
        shift # past argument=value
        ;;
        -s=*)
        SHARED="${i#*=}"
        shift # past argument=value
        ;;
        -t=*)
        SUT="${i#*=}"
        shift # past argument=value
        ;;
        *)
          # unknown option
        ;;
    esac
done
echo "DOCKERGID = $DOCKERGID"
echo "IMAGE = $IMAGE"
echo "APP = $APP"
echo "SHARED = $SHARED"
echo "SUT = $SUT"

if [[ -z $IMAGE ]]; then
    echo "error: -i, docker image is not specified"
fi

if [[ -z $SUT ]]; then
    echo "error: -t option is not give or empty"
    exit 1
fi

if ! [[ -d $SHARED ]]; then
    echo "error: -s, $SHARED does not exist"
    exit 1
fi

if ! [[ -d ../$SUT ]]; then
    echo "error: could not find a tool test at ../$SUT"
    exit 1
fi 

echo "Copying a tool to test from ../$SUT"
rm -rf ./$SUT
cp -R ../$SUT .

echo "Cleaning shared directories"
rm -rf $SHARED/$SUT
mkdir $SHARED/$SUT
docker stop $APP
docker rm $APP
docker rmi -f $IMAGE
docker build --rm -t $IMAGE .
docker run -v /var/run/docker.sock:/var/run/docker.sock -v $SHARED/$SUT:/var/jenkins_home/report/ -e MASTER_SSH_PORT=22 -e MASTER_SLAVE_USER=jenkins -e MASTER_SLAVE_PWD=jenkins -e DOCKER_GID=$DOCKERGID --name $APP $IMAGE

#docker run -i -v /var/run/docker.sock:/var/run/docker.sock -v $HOME/$SHARED:/var/jenkins_home -e MASTER_SSH_PORT=22 -e MASTER_SLAVE_USER=jenkins -e MASTER_SLAVE_PWD=jenkins -e DOCKER_GID=998 --name $APP $IMAGE
#docker run -v /var/run/docker.sock:/var/run/docker.sock -v $HOME/$SHARED/$SUT:/var/jenkins_home/report/ -e MASTER_SSH_PORT=22 -e MASTER_SLAVE_USER=jenkins -e MASTER_SLAVE_PWD=jenkins -e DOCKER_GID=$DOCKERGID --name $APP $IMAGE
#docker run -d -v /var/run/docker.sock:/var/run/docker.sock -e MASTER_SSH_PORT=22 -e MASTER_SLAVE_USER=jenkins -e MASTER_SLAVE_PWD=jenkins -e DOCKER_GID=998 --name $APP $IMAGE
#docker exec -it $APP bash -c "su - jenkins"
#docker exec -it $APP bash
