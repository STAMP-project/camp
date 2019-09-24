#!/usr/bin/env bash

LANGUAGE="java" # set this variable to anything else if your app is not Java-based
FREQS=(15013)   # 16103 17203 18301) #(97 193 283) # Frequencies, in Hz, at which the profiler will be executed
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

  cd $DIR/configs/sql
  docker build -t ow2/mysql:latest .

  cd $DIR

  cd $DIR/configs/config0
  docker build -t ow2/lutece:latest --build-arg PROFILER_FREQ=$FREQ .


  cd $DIR

  cd $DIR/configs/config1
  docker build -t ow2/lutece2:latest --build-arg PROFILER_FREQ=$FREQ .

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

  timeout -k 60s 100s docker run -v $LOGDIR:/data --cap-add=ALL --network="ow2" --name lutece ow2/lutece:latest -v $LOGDIR:/data >> $LOGDIR/out.log


  if [ "$LANGUAGE" == "java" ]; then
    $FLAMEGRAPH_DIR/stackcollapse-ljp.awk < $LOGDIR/traces.txt >> $LOGDIR/java.folded
    cp $LOGDIR/*.map /tmp/.
    #cat $LOGDIR/java.folded >> $PROFDIR/java.folded
  fi

  #for some reasons, does not work inside the container... we need to run it locally...
  perf script -i $LOGDIR/perf.data > $LOGDIR/out.perf
  $FLAMEGRAPH_DIR/stackcollapse-perf.pl $LOGDIR/out.perf >> $LOGDIR/generic.folded
  #cat $LOGDIR/generic.folded >> $PROFDIR/generic.folded

  if [ "$LANGUAGE" == "java" ]; then
    rm -f /tmp/*.map
  fi


  docker rm -f lutece
  docker rm -f lutece2
  docker rm -f storage

  docker rmi -f ow2/lutece:latest
  docker rmi -f ow2/lutece2:latest
  docker rmi -f ow2/mysql:latest

}


echo "---- Building and Running all configurations at all frequencies ----"
for INDEX in $(seq 0 2); do
  mkdir -p $DIR/configs/config$INDEX/profiling
	
	for FREQ in ${FREQS[@]}; do 

	  build $INDEX $FREQ
	  run $INDEX $FREQ

	done
done
wait
echo "---- Cleaning a bit ----"
#docker rmi -f  tracedconfig
#docker rmi -f $(docker images -q --filter "dangling=true")





#############################################################
##### Cleaning profiling traces and extracting a metric #####
#############################################################

function fg
{
  INPUTFILE=$1

  $FLAMEGRAPH_DIR/flamegraph.pl $INPUTFILE > $INPUTFILE.svg
  echo "Flame graph SVG written to $INPUTFILE.svg"
}


#clean and re-align traces and remove duplicates
function sort_and_clean
{
  INPUTFILE=$1
  rm -rf $INPUTFILE.clean
  rm -rf $INPUTFILE.clean.sorted
  #FIXME: this function needs to be improved...

  while read line; do
    line=${line#*;} #remove the first two frames (typically irrelevant, like Thread-1 in Java)
    line=${line#*;}
    line=${line% *} #remove last digit and replace it by 1
    echo "$line" >> $INPUTFILE.clean  #remove number at the end of the line
  done < $INPUTFILE

  sed -i 's/\[.*\]//g' $INPUTFILE.clean #remove all crap between [...] with sed
  sed -i 's/Interpreter//g' $INPUTFILE.clean
  sed -i 's/[0-9]//g' $INPUTFILE.clean #remove all numbers to avoid execution-specific IDs in traces
  sed -i 's/\.\./\./g' $INPUTFILE.clean #replace .. by . (can happen once numbers have been removed)
  sed -i 's/;;*/;/g' $INPUTFILE.clean #replace ;* by ;
  sed -i 's/^;//g' $INPUTFILE.clean #remove ; if that is the first character on a line
  sed -i 's/$/ 1/' $INPUTFILE.clean

  sort $INPUTFILE.clean | uniq -u >$INPUTFILE.clean.sorted
}

function metric
{
  INDEX=$1
  DIFFMODE=$2

  ALL=$(wc -l $PROFDIR/all.$DIFFMODE.clean.sorted | awk '{ print $1 }')
  CURRENT=$(wc -l $DIR/configs/config$INDEX/profiling/$DIFFMODE.folded.clean.sorted | awk '{ print $1 }')
  OP="scale=2; $CURRENT/$ALL*100"
  RESULT=$(bc -l <<< $OP)
  echo "Configuration $INDEX contributed $CURRENT/$ALL = $RESULT % of all unique traces" >> $PROFDIR/metrics.$DIFFMODE.log

  $FLAMEGRAPH_DIR/difffolded.pl -n -s $PROFDIR/all.$DIFFMODE.clean.sorted $DIR/configs/config$INDEX/profiling/$DIFFMODE.folded.clean.sorted > $DIR/configs/config$INDEX/profiling/$DIFFMODE.diff
  $FLAMEGRAPH_DIR/flamegraph.pl $DIR/configs/config$INDEX/profiling/$DIFFMODE.diff > $DIR/configs/config$INDEX/profiling/$DIFFMODE.diff.svg
}

echo "---- Doing some heavy science ----"
for INDEX in $(seq 0 2); do
  sort_and_clean $DIR/configs/config$INDEX/profiling/generic.folded
  fg $DIR/configs/config$INDEX/profiling/generic.folded.clean.sorted
  cp $DIR/configs/config$INDEX/profiling/generic.folded.clean.sorted $PROFDIR/$INDEX.generic
  if [ "$LANGUAGE" == "java" ]; then
    sort_and_clean $DIR/configs/config$INDEX/profiling/java.folded
    fg $DIR/configs/config$INDEX/profiling/java.folded.clean.sorted
    cp $DIR/configs/config$INDEX/profiling/java.folded.clean.sorted $PROFDIR/$INDEX.java
  fi
done
cat $PROFDIR/*.generic >> $PROFDIR/all.generic
sort $PROFDIR/all.generic | uniq -u >$PROFDIR/all.generic.clean.sorted
fg $PROFDIR/all.generic.clean.sorted
if [ "$LANGUAGE" == "java" ]; then
  cat $PROFDIR/*.java >> $PROFDIR/all.java
  sort $PROFDIR/all.java | uniq -u >$PROFDIR/all.java.clean.sorted
  fg $PROFDIR/all.java.clean.sorted
fi

for INDEX in $(seq 0 2); do
  metric $INDEX "generic"
  if [ "$LANGUAGE" == "java" ]; then
    metric $INDEX "java"
  fi
done

echo "---- Java traces ----"
cat $PROFDIR/metrics.java.log
echo "---- System traces ----"
cat $PROFDIR/metrics.generic.log

rm -rf $DIR/FlameGraph

