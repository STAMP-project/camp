FROM camp/runtime

ENV JETTY_VERSION=9.3.27.v20190418
ENV JETTY_ARCHIVE= https://repo1.maven.org/maven2/org/eclipse/jetty/jetty-distribution/${JETTY_VERSION}/jetty-distribution-${JETTY_VERSION}.zip

ENV JETTY_HOME=/usr/local/jetty

ENV WEBAPPS=${JETTY_HOME}/webapps

RUN apt-get -y update \
        && apt-get -y upgrade \
        && apt-get -y install wget \
        && 

RUN mkdir ${JETTY_HOME} \
        && wget ${JETTY_ARCHIVE} -O /tmp/jetty.zip \
        && cd /tmp && unzip jetty.zip \
        && cp -Rv /tmp/jetty-distribution-${JETTY_VERSION}/* ${JETTY_HOME}

EXPOSE 8080

CMD ["java","-jar","/usr/local/jetty/start.jar"]




