#!/usr/bin/env bash

LANGUAGE="java" # set this variable to anything else if your app is not Java-based
FREQS=(15013 16103 17203 18301) #(97 193 283) # Frequencies, in Hz, at which the profiler will be executed
DIR=$(pwd)

# create a global dir to aggregate all traces
rm -rf $DIR/configs/profiling
mkdir -p $DIR/configs/profiling
PROFDIR=$DIR/configs/profiling

for INDEX in $(seq 0 2); do
  rm -rf $DIR/configs/config$INDEX/profiling
done


# Install Flamegraph locally, we'll use some of their scripts
echo "---- Installing FlameGraph ----"
mkdir -p $DIR/FlameGraph
git clone https://github.com/brendangregg/FlameGraph.git $DIR/FlameGraph
FLAMEGRAPH_DIR=$DIR/FlameGraph



############################################################
##### Building and Running instrumented configurations #####
############################################################

#$1: index of the configuration
#$2: frequency (in Hz) at which the profiler will be executed
function build
{

  docker network rm ow2

  INDEX=$1
  FREQ=$2

  cd $DIR/configs/config0
  docker build -t ow2/lutece:latest --build-arg PROFILER_FREQ=$FREQ .

  cd $DIR

  cd $DIR/configs/config1
  docker build -t ow2/mysql:latest --build-arg PROFILER_FREQ=$FREQ .

  cd $DIR

  docker network create ow2

}

#$1: index of the configuration
#$2: frequency (in Hz) at which the profiler will be executed
function run
{
  INDEX=$1
  FREQ=$2

  LOGDIR=$DIR/configs/config$INDEX/profiling

  docker run -d --name storage --network="ow2" ow2/mysql:latest

  sleep 10

  timeout -k 60s 100s docker run -v $LOGDIR:/data --cap-add=ALL --network="ow2" --name lutece ow2/lutece:latest >> $LOGDIR/out.log
  docker rm -f lutece
  docker rm -f storage

  docker rmi -f ow2/lutece:latest
  docker rmi -f ow2/mysql:latest

}


echo "---- Building and Running all configurations at all frequencies ----"
for INDEX in $(seq 0 2); do
  mkdir -p $DIR/configs/config$INDEX/profiling


  build $INDEX $FREQ
  run $INDEX $FREQ

done
wait
echo "---- Cleaning a bit ----"
#docker rmi -f  tracedconfig
#docker rmi -f $(docker images -q --filter "dangling=true")


#DELETE FOR STRACE


#############################################################
##### Cleaning profiling traces and extracting a metric #####
#############################################################

