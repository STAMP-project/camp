#!/bin/bash
# get HOST_ADDRESS for my SQL Config
# HOST_ADDRESS="$(ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1')"

HOST_ADDRESS="<YOUR_ADDRESS>"
# use this command to get your IP address: ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'
echo "myhost"$HOST_ADDRESS
# add jdbc mysql connector 
curl -LO https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-8.0.15.zip
unzip mysql-connector-java-8.0.15.zip -d connectorj
cp connectorj/mysql-connector-java-8.0.15/mysql-connector-java-8.0.15.jar addons/
ls addons/

# HashMap for scheduler config
# ~/config/scheduler/database.properties
declare -A scheduler
scheduler["hibernate.connection.driver_class"]="com.mysql.cj.jdbc.Driver"
scheduler["hibernate.connection.url"]="jdbc:mysql://"$HOST_ADDRESS":3306/scheduler?verifyServerCertificate=false\&useSSL=false\&useLegacyDatetimeCode=false\&serverTimezone=UTC"
scheduler["hibernate.dialect"]="org.hibernate.dialect.MySQL5InnoDBDialect"
scheduler["hibernate.connection.username"]="scheduler"
scheduler["hibernate.connection.password"]="scheduler"

# HashMap for rm config
# ~/config/rm/database.properties
declare -A rm
rm["hibernate.connection.driver_class"]="com.mysql.cj.jdbc.Driver"
rm["hibernate.connection.url"]="jdbc:mysql://"$HOST_ADDRESS":3306/rm?verifyServerCertificate=false\&useSSL=false\&useLegacyDatetimeCode=false\&serverTimezone=UTC"
rm["hibernate.dialect"]="org.hibernate.dialect.MySQL5InnoDBDialect"
rm["hibernate.connection.username"]="rm"
rm["hibernate.connection.password"]="rm"

# HashMap for catalog config
# ~/dist/war/catalog/WEB-INF/classes/application.properties
declare -A catalog
catalog["spring.datasource.url"]="jdbc:mysql://"$HOST_ADDRESS":3306/catalog?verifyServerCertificate=false\&useSSL=false\&useLegacyDatetimeCode=false\&serverTimezone=UTC"
catalog["spring.datasource.username"]="catalog"
catalog["spring.datasource.password"]="catalog"
catalog["spring.datasource.driverClassName"]="com.mysql.cj.jdbc.Driver"
catalog["spring.jpa.database-platform"]="org.hibernate.dialect.MySQL5InnoDBDialect"

# HashMap for scheduling config
# ~/dist/war/scheduling-api/WEB-INF/classes/application.properties
declare -A scheduling
scheduling["spring.datasource.url"]="jdbc:mysql://"$HOST_ADDRESS":3306/scheduler?verifyServerCertificate=false\&useSSL=false\&useLegacyDatetimeCode=false\&serverTimezone=UTC"
scheduling["spring.datasource.username"]="scheduler"
scheduling["spring.datasource.password"]="scheduler"
scheduling["spring.datasource.driver-class-name"]="com.mysql.cj.jdbc.Driver"
scheduling["spring.jpa.database-platform"]="org.hibernate.dialect.MySQL5InnoDBDialect"

# HashMap for job planner config
# ~/dist/war/job-planner/WEB-INF/classes/application.properties
declare -A jp
jp["spring.datasource.url"]="jdbc:mysql://"$HOST_ADDRESS":3306/scheduler?verifyServerCertificate=false\&useSSL=false\&useLegacyDatetimeCode=false\&serverTimezone=UTC"
jp["spring.datasource.username"]="scheduler"
jp["spring.datasource.password"]="scheduler"
jp["spring.datasource.driver-class-name"]="com.mysql.cj.jdbc.Driver"
jp["spring.jpa.database-platform"]="org.hibernate.dialect.MySQL5InnoDBDialect"

# HashMap for pcw config
# ~/dist/war/proactive-cloud-watch/WEB-INF/classes/application.properties
declare -A pcw
pcw["spring.datasource.url"]="jdbc:mysql://"$HOST_ADDRESS":3306/scheduler?verifyServerCertificate=false\&useSSL=false\&useLegacyDatetimeCode=false\&serverTimezone=UTC"
pcw["spring.datasource.username"]="scheduler"
pcw["spring.datasource.password"]="scheduler"
pcw["spring.datasource.driver-class-name"]="com.mysql.cj.jdbc.Driver"
pcw["spring.jpa.database-platform"]="org.hibernate.dialect.MySQL5InnoDBDialect"

# Change config of dist/war/catalog/WEB-INF/classes/application.properties
for key in ${!scheduler[@]}
do
grep -q '^'$key'' config/scheduler/database.properties && sed -i 's|^'$key'.*|'$key'='${scheduler[$key]}'|' config/scheduler/database.properties || echo "
$key"="${scheduler[$key]}" >> config/scheduler/database.properties
done

# Change config of dist/war/catalog/WEB-INF/classes/application.properties
for key in ${!rm[@]}
do
grep -q '^'$key'' config/rm/database.properties && sed -i 's|^'$key'.*|'$key'='${rm[$key]}'|' config/rm/database.properties || echo "
$key"="${rm[$key]}" >> config/rm/database.properties
done

# Change config of dist/war/catalog/WEB-INF/classes/application.properties
for key in ${!catalog[@]}
do
grep -q '^'$key'' dist/war/catalog/WEB-INF/classes/application.properties && sed -i 's|^'$key'.*|'$key'='${catalog[$key]}'|' dist/war/catalog/WEB-INF/classes/application.properties || echo "
$key"="$(sed 's/\\//g' <<< "${catalog[$key]}")" >> dist/war/catalog/WEB-INF/classes/application.properties
done

# Change config of dist/war/scheduling-api/WEB-INF/classes/application.properties
for key in ${!scheduling[@]}
do
grep -q '^'$key'' dist/war/scheduling-api/WEB-INF/classes/application.properties && sed -i 's|^'$key'.*|'$key'='${scheduling[$key]}'|' dist/war/scheduling-api/WEB-INF/classes/application.properties || echo "
$key"="${scheduling[$key]}" >> dist/war/scheduling-api/WEB-INF/classes/application.properties
done

# Change config of dist/war/job-planner/WEB-INF/classes/application.properties
for key in ${!jp[@]}
do
grep -q '^'$key'' dist/war/job-planner/WEB-INF/classes/application.properties && sed -i 's|^'$key'.*|'$key'='${jp[$key]}'|' dist/war/job-planner/WEB-INF/classes/application.properties || echo "
$key"="${jp[$key]}" >> dist/war/job-planner/WEB-INF/classes/application.properties
done

# Change config of dist/war/proactive-cloud-watch/WEB-INF/classes/application.properties
for key in ${!pcw[@]}
do
grep -q '^'$key'' dist/war/proactive-cloud-watch/WEB-INF/classes/application.properties && sed -i 's|^'$key'.*|'$key'='${pcw[$key]}'|' dist/war/proactive-cloud-watch/WEB-INF/classes/application.properties || echo "
$key"="$(sed 's/\\//g' <<< "${pcw[$key]}")" >> dist/war/proactive-cloud-watch/WEB-INF/classes/application.properties
done

#add jdbc mysql connector 
#curl -LO https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-8.0.15.zip
#unzip mysql-connector-java-8.0.15.zip -d connectorj
#cp connectorj/mysql-connector-java-8.0.15/mysql-connector-java-8.0.15.jar addons/
