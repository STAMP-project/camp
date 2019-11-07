#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#

FROM camp/runtime

ARG TOMCAT_MAJOR=7
ARG TOMCAT_REVISION=0.96
ARG TOMCAT_VERSION=${TOMCAT_MAJOR}.${TOMCAT_REVISION}
ARG TOMCAT_ARCHIVE=http://archive.apache.org/dist/tomcat/tomcat-${TOMCAT_MAJOR}/v${TOMCAT_VERSION}/bin/apache-tomcat-${TOMCAT_VERSION}.tar.gz

ENV TOMCAT_HOME=/usr/local/tomcat

ENV WEBAPPS=${TOMCAT_HOME}/webapps

RUN apt-get -y update \
        && apt-get -y upgrade \
        && apt-get -y install wget

RUN mkdir ${TOMCAT_HOME} \
        && wget ${TOMCAT_ARCHIVE} -O /tmp/tomcat.tar.gz \
        && cd /tmp && tar xvfz tomcat.tar.gz \
        && cp -Rv /tmp/apache-tomcat-${TOMCAT_VERSION}/* ${TOMCAT_HOME}

EXPOSE 8080

CMD ${TOMCAT_HOME}/bin/catalina.sh run

