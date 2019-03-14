FROM tomcat:8-jre8

LABEL maintainer "franck.chauvel@sintef.no"

# Move the WebApp contents into the webapp folder
ADD target/greetings-1.0-SNAPSHOT.war /usr/local/tomcat/webapps/
RUN mv /usr/local/tomcat/webapps/greetings-1.0-SNAPSHOT.war /usr/local/tomcat/webapps/greetings.war

CMD ["catalina.sh", "run"]
