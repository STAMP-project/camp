FROM debian:stretch

# install needed apps
RUN apt-get update && apt-get dist-upgrade -y && \
    apt-get install -y mysql-client default-jdk ant maven git tomcat8 --no-install-recommends

# define the fully qualified artifact of the site
ARG site=site-forms-demo-1.0.0-SNAPSHOT

# build the site and assemble the webapp
WORKDIR /app

ADD pom.xml /app/pom.xml

RUN mvn lutece:site-assembly

ADD db.properties /app/target/${site}/WEB-INF/conf/db.properties

RUN mv /app/target/${site}/ /var/lib/tomcat8/webapps/site-forms-demo

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["sh", "/entrypoint.sh"]
