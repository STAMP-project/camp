#!/bin/bash

BASEDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

rm -rf $BASEDIR/out
rm -rf $BASEDIR/out_all_refined2

docker pull fchauvel/camp

echo "XP all (refined)"
echo "------"
cp camp.yaml.3 camp.yaml
docker run -v $BASEDIR:/camp fchauvel/camp camp generate --all -d .
docker run -v $BASEDIR:/camp fchauvel/camp camp realize -d .
docker run -v /var/run/docker.sock:/var/run/docker.sock -v $BASEDIR:/camp fchauvel/camp camp execute -d .
mv $BASEDIR/out $BASEDIR/out_all_refined2
rm camp.yaml

docker rm -f $(docker ps -aq)
docker rmi -f $(docker images -aq)
