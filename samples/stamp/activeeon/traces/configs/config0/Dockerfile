FROM openjdk:8

ARG PROFILER_FREQ 

RUN echo "$PROFILER_FREQ" > /.profiler

RUN apt update

RUN apt-get install -y build-essential cmake wget unzip flex bison && rm -rf /var/lib/apt/lists/*

RUN cd /root && git clone https://github.com/jvm-profiling-tools/perf-map-agent.git

RUN cd /root/perf-map-agent && cmake . && make

RUN cd /root/perf-map-agent && cp out/libperfmap.so /libperfmap.so && cp out/attach-main.jar /libperfagent.jar

RUN cd /root && wget https://github.com/dcapwell/lightweight-java-profiler/archive/master.zip && unzip master.zip && rm -f master.zip

RUN cd /root/lightweight-java-profiler-master && sed -i "s/static const int kNumInterrupts = 100;/static const int kNumInterrupts = $PROFILER_FREQ;/" src/globals.h && make

RUN cp /root/lightweight-java-profiler-master/build-64/liblagent.so /liblagent.so

RUN wget https://github.com/torvalds/linux/archive/v5.1.zip && unzip v5.1.zip && rm v5.1.zip

RUN cd linux-5.1/tools/perf && make && cp perf /usr/bin

COPY . .

CMD ["/bin/sh", "run.sh"]
