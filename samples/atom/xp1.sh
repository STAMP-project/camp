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
rm -rf $BASEDIR/out7
rm -rf $BASEDIR/out8
rm -rf $BASEDIR/out9
rm -rf $BASEDIR/out10
rm -rf $BASEDIR/out11

docker pull fchauvel/camp
# cd $BASEDIR/../..
# docker build -t fchauvel/camp .
# cd $BASEDIR

for i in `seq 0 11`;
do
  echo "XP" $i
  echo "------"
  cp camp$i.yaml.ori camp.yaml
  docker run -v $BASEDIR:/camp fchauvel/camp camp generate --all -d .
  docker run -v $BASEDIR:/camp fchauvel/camp camp realize -d .

  #docker run -v /var/run/docker.sock:/var/run/docker.sock -v $BASEDIR:/camp fchauvel/camp camp execute -d .
  declare -i i
  i+=1
  for d in $(ls -d -- $BASEDIR/out/) ; do
    cd $d/config_$i/images/atom_0
    (docker build -t bmorin/atom-$i .) 2>&1 | tee ../../test.log
    docker rmi -f bmorin/atom-$i
    sed -n -e '/passing/,$p' ../../test.log > ../../test_results.log
    i+=1
  done

  mv $BASEDIR/out $BASEDIR/out$i
  rm camp.yaml
done

docker rm -f $(docker ps -aq)
docker rmi -f $(docker images -aq)
