#!/bin/bash

BASEDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

rm -rf $BASEDIR/out
rm -rf $BASEDIR/out0
rm -rf $BASEDIR/out1
rm -rf $BASEDIR/out2
rm -rf $BASEDIR/out3
rm -rf $BASEDIR/out4
rm -rf $BASEDIR/out5
rm -rf $BASEDIR/out6

docker pull fchauvel/camp
# cd $BASEDIR/../..
# docker build -t fchauvel/camp .
# cd $BASEDIR

for i in `seq 0 6`;
do
  echo "XP" $i
  echo "------"
  cp camp$i.yaml camp.yaml
  docker run -v $BASEDIR:/camp fchauvel/camp camp generate --all -d .
  docker run -v $BASEDIR:/camp fchauvel/camp camp realize -d .
  docker run -v /var/run/docker.sock:/var/run/docker.sock -v $BASEDIR:/camp fchauvel/camp camp execute -d .
  mv $BASEDIR/out $BASEDIR/out$i
  rm camp.yaml
done

docker rm -f $(docker ps -aq)
docker rmi -f $(docker images -aq)
