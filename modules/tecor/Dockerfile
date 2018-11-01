#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# See the NOTICE file distributed with this work for additional
# information regarding copyright ownership.
#

FROM jenkins:2.32.1
LABEL maintainer "Anatoly Vasilevskiy <Anatoly.Vasilevskiy@sintef.no>"

USER root

RUN apt-get update && \
    apt-get install -y openssl sshpass openssh-server git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN echo 'jenkins:jenkins' | chpasswd \
	&& mkdir /var/run/sshd	

#copy everithing in the current folder
#requires that the tool to test is packaged together with the testing tool
COPY . "$JENKINS_HOME"/

#starup scritp, runs sshd and than jenkins.sh from jenkins:latest
COPY startup.sh /usr/local/bin/startup.sh
RUN chmod a+x /usr/local/bin/startup.sh

#installing docker START
ENV DOCKER_BUCKET get.docker.com
ENV DOCKER_VERSION 1.13.0
ENV DOCKER_SHA256 fc194bb95640b1396283e5b23b5ff9d1b69a5e418b5b3d774f303a7642162ad6
#ENV DOCKER_VERSION 1.12.6
#ENV DOCKER_SHA256 cadc6025c841e034506703a06cf54204e51d0cadfae4bae62628ac648d82efdd

RUN set -x \
	&& curl -fSL "https://${DOCKER_BUCKET}/builds/Linux/x86_64/docker-${DOCKER_VERSION}.tgz" -o docker.tgz \
	&& echo "${DOCKER_SHA256} *docker.tgz" | sha256sum -c - \
	&& tar -xzvf docker.tgz \
	&& mv docker/* /usr/local/bin/ \
	&& rmdir docker \
	&& rm docker.tgz \
	&& docker -v

#installing docker END

CMD ["/usr/local/bin/startup.sh"]
