#!/bin/bash
set -e
#set -x

CUR_DIR=`pwd`
PID=$1
OPTIONS=$2
ATTACH_JAR=attach-main.jar
PERF_MAP_DIR=$(dirname $(readlink -f $0))/..
ATTACH_JAR_PATH=$PERF_MAP_DIR/out/$ATTACH_JAR
PERF_MAP_FILE=/tmp/perf-$PID.map

#if [ -z "$JAVA_HOME" ]; then
#  JAVA_HOME=/usr/lib/jvm/default-java
#fi

#[ -d "$JAVA_HOME" ] || JAVA_HOME=/etc/alternatives/java_sdk
#[ -d "$JAVA_HOME" ] || (echo "JAVA_HOME directory at '$JAVA_HOME' does not exist." && false)
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/

rm $PERF_MAP_FILE -f
(cd $PERF_MAP_DIR/out && java -cp $ATTACH_JAR_PATH:$JAVA_HOME/lib/tools.jar net.virtualvoid.perf.AttachOnce $PID "$OPTIONS")
chown root:root $PERF_MAP_FILE
