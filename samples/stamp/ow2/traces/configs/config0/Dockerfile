FROM debian:stretch

ARG PROFILER_FREQ

RUN echo "$PROFILER_FREQ" > /.profiler

RUN apt update

# install needed apps
RUN apt-get update && apt-get dist-upgrade -y && \
    apt-get install -y mysql-client default-jdk ant maven git tomcat8 --no-install-recommends

RUN apt-get install -y build-essential cmake wget unzip flex bison && rm -rf /var/lib/apt/lists/*

RUN cd /root && git clone https://github.com/jvm-profiling-tools/perf-map-agent.git

RUN cd /root/perf-map-agent && cmake . && make

RUN cd /root/perf-map-agent && cp out/libperfmap.so /libperfmap.so && cp out/attach-main.jar /libperfagent.jar

RUN cd /root && wget https://github.com/dcapwell/lightweight-java-profiler/archive/master.zip && unzip master.zip && rm -f master.zip

RUN cd /root/lightweight-java-profiler-master && sed -i "s/static const int kNumInterrupts = 100;/static const int kNumInterrupts = $PROFILER_FREQ;/" src/globals.h && make

RUN cp /root/lightweight-java-profiler-master/build-64/liblagent.so /liblagent.so

RUN wget https://github.com/torvalds/linux/archive/v5.1.zip && unzip v5.1.zip && rm v5.1.zip

RUN cd linux-5.1/tools/perf && make && cp perf /usr/bin


# define the fully qualified artifact of the site
ARG site=site-forms-demo-1.0.0-SNAPSHOT

# build the site and assemble the webapp
WORKDIR /app

ADD pom.xml /app/pom.xml

RUN mvn clean install && mvn lutece:site-assembly

ADD db.properties /app/target/${site}/WEB-INF/conf/db.properties

RUN mv /app/target/${site}/ /var/lib/tomcat8/webapps/site-forms-demo

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["sh", "/entrypoint.sh"]
