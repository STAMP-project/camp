#!/bin/bash

BASEDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

rm -rf $BASEDIR/out
rm -rf $BASEDIR/out_coverage

docker pull fchauvel/camp

echo "XP coverage"
echo "------"
cp camp.yaml.ori camp.yaml
docker run -v $BASEDIR:/camp fchauvel/camp camp generate --coverage -d .
docker run -v $BASEDIR:/camp fchauvel/camp camp realize -d .

#workaround https://github.com/STAMP-project/camp/issues/57
cd out
for d in */ ; do
  cd $BASEDIR/out/$d/images/sphinx_0
  sed -i '/cmdclass=cmdclass,/Q' src/setup.py
  echo "  cmdclass=cmdclass,
  )" >> src/setup.py
done
cd $BASEDIR
#end workaround

docker run -v /var/run/docker.sock:/var/run/docker.sock -v $BASEDIR:/camp fchauvel/camp camp execute -d .
mv $BASEDIR/out $BASEDIR/out_coverage
rm camp.yaml

docker rm -f $(docker ps -aq)
docker rmi -f $(docker images -aq)
