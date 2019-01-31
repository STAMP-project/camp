FROM ubuntu

# Install dependencies
RUN echo "deb http://archive.ubuntu.com/ubuntu trusty main universe" > /etc/apt/sources.list
RUN apt-get -y update
RUN apt-get install -y curl


# Install proactive server last version from jenkins
COPY get-last-proactive-secret-do-not-commit.sh /root/get-last-proactive-secret-do-not-commit.sh
RUN chmod 755 /root/get-last-proactive-secret-do-not-commit.sh
RUN /root/get-last-proactive-secret-do-not-commit.sh
RUN cd /root && unzip proactive.zip

# Install system tests
RUN apt-get install gradle jdk etc...
