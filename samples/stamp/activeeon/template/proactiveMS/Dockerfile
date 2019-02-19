FROM ubuntu

# Install dependencies
RUN apt update && apt install -y \
    apt-transport-https \
    apt-utils \
    wget \
    unzip \
    openjdk-8-jdk-headless \
    openjdk-8-jre-headless
RUN echo "deb http://archive.ubuntu.com/ubuntu trusty main universe" > /etc/apt/sources.list
RUN apt-get -y update
RUN apt-get install -y curl
RUN apt-get install unzip

# Install proactive server 8.5.0 version from jenkins
COPY get-last-proactive-secret-do-not-commit.sh /root/get-last-proactive-secret-do-not-commit.sh
RUN chmod +x /root/get-last-proactive-secret-do-not-commit.sh
RUN /root/get-last-proactive-secret-do-not-commit.sh
COPY activeeon_proactive_server_entrypoint.sh /root/activeeon_proactive_server_entrypoint.sh
RUN chmod +x /root/activeeon_proactive_server_entrypoint.sh

RUN cd /root/ && unzip proactive.zip -d proactive
RUN chmod -R 755 /root/proactive/activeeon_enterprise-pca_server-linux-x64-8.5.0-SNAPSHOT/bin/proactive-server

WORKDIR /root/proactive/activeeon_enterprise-pca_server-linux-x64-8.5.0-SNAPSHOT/

# Remove -Xms4g parameter option to make PA working inside docker
RUN sed -i 's/"-Xms4g"//g' bin/proactive-server

COPY change-proactive-db-config.sh /root/proactive/activeeon_enterprise-pca_server-linux-x64-8.5.0-SNAPSHOT/

RUN chmod 755 change-proactive-db-config.sh

RUN ./change-proactive-db-config.sh

EXPOSE 8080

CMD ["/root/activeeon_proactive_server_entrypoint.sh"]
