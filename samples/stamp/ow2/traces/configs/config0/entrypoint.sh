#!/bin/bash

# Start Tomcat
/usr/lib/jvm/default-java/bin/java -Djava.util.logging.config.file=/var/lib/tomcat8/conf/logging.properties -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager -Djava.awt.headless=true -Xmx512m -XX:+UseConcMarkSweepGC -Djdk.tls.ephemeralDHKeySize=2048 -Djava.endorsed.dirs=/usr/share/tomcat8/endorsed -classpath /usr/share/tomcat8/bin/bootstrap.jar:/usr/share/tomcat8/bin/tomcat-juli.jar -Dcatalina.base=/var/lib/tomcat8 -Dcatalina.home=/usr/share/tomcat8 -Djava.io.tmpdir=/tmp/tomcat8-tomcat8-tmp org.apache.catalina.startup.Bootstrap start  & PID=$!

java -cp /libperfagent.jar:$JAVA_HOME/lib/tools.jar net.virtualvoid.perf.AttachOnce $PID

sleep 60

# /activeeon_enterprise-pca_server-linux-x64-8.5.0-SNAPSHOT/bin/proactive-client -s /workflow-test.xml

PROFILER_FREQ=$(cat /.profiler)
perf record -e cpu-clock -F $PROFILER_FREQ -p $PID -a -g -o /data/perf.data


cp /tmp/perf*.map /data/perf-$PID.map

#Ikill -SIGINT $PID

/usr/lib/jvm/default-java/bin/java -Djava.util.logging.config.file=/var/lib/tomcat8/conf/logging.properties -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager -Djava.awt.headless=true -Xmx512m -XX:+UseConcMarkSweepGC -Djdk.tls.ephemeralDHKeySize=2048 -Djava.endorsed.dirs=/usr/share/tomcat8/endorsed -classpath /usr/share/tomcat8/bin/bootstrap.jar:/usr/share/tomcat8/bin/tomcat-juli.jar -Dcatalina.base=/var/lib/tomcat8 -Dcatalina.home=/usr/share/tomcat8 -Djava.io.tmpdir=/tmp/tomcat8-tomcat8-tmp org.apache.catalina.startup.Bootstrap stop

sleep 60

kill -INT $PID

cp traces.txt /data/traces.txt

chmod -R 777 /data
