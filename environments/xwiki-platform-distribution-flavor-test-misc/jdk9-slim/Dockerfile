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

FROM maven:3.5.2-jdk-9-slim
MAINTAINER Anatoly Vasilevskiy <Anatoly.Vasilevskiy@sintef.no>

RUN mkdir workingdir \
	&& apt-get -qq update \
	&& apt-get install --no-install-recommends -qqy \
	sshpass \
	ca-certificates \
	openssh-server \
	ant \
	ant-optional \
	python2.7 && \
	ln -s /usr/bin/python2.7 /usr/bin/python

#copy everything
COPY settings.xml /root/.m2/settings.xml
COPY . workingdir/

#COPY dojob.py workingdir/dojob.py
RUN chmod a+x workingdir/dojob.py
WORKDIR workingdir
