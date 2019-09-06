/activeeon_enterprise-pca_server-linux-x64-8.5.0-SNAPSHOT/bin/proactive-server &
PID=$!
#java -jar /libperfagent.jar $PID &
#sleep 100000000000000000000000000000
#perf record
#PROFILER_FREQ=$(cat /.profiler)
#sleep 500

java -cp /libperfagent.jar:$JAVA_HOME/lib/tools.jar net.virtualvoid.perf.AttachOnce $PID

sleep 500

/activeeon_enterprise-pca_server-linux-x64-8.5.0-SNAPSHOT/bin/proactive-client -s /workflow-test.xml

PROFILER_FREQ=$(cat /.profiler)
perf record -e cpu-clock -F $PROFILER_FREQ -p $PID -a -g -o /data/perf.data -- sleep 300


cp /tmp/perf*.map /data/perf-$PID.map

#Ikill -SIGINT $PID 

#kill -INT $PID

/activeeon_enterprise-pca_server-linux-x64-8.5.0-SNAPSHOT/bin/proactive-client -shutdown
sleep 60
cp traces.txt /data/traces.txt

chmod -R 777 /data

