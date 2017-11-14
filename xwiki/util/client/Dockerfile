FROM openjdk:8-jdk

RUN apt-get update && \
    apt-get --no-install-recommends -y install \
    maven 

WORKDIR /root

RUN git clone https://github.com/songhui/xwikismoke && \
    mkdir /root/.m2 && \
    cp -f /root/xwikismoke/settings.xml /root/.m2/settings.xml

WORKDIR /root/xwikismoke

RUN mvn clean install

CMD ["mvn", "install"]
