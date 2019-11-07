#!/bin/bash

JAVA_OPTIONS=-Xmx512m \
    -XX:+UseConcMarkSweepGC

java ${JAVA_OPTIONS} -jar ${JETTY_HOME}/start.jar
