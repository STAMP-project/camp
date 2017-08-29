#!/bin/bash -e
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


#checking if ssh server is running
#SSDPID=$(pidof sshd)
#[ $? -eq 0 ] && echo "SUCCESS: ssh daemon" || echo "FAILURE: ssh daemon"

#setting up permissions for docker.sock
if ! grep -q docker /etc/group; then
  if [[ -e "/var/run/docker.sock" ]] && [[ -n "$DOCKER_GID" ]] ; then
  	echo "Setting permissions for docker.sock"
  	groupadd -g "$DOCKER_GID" docker
  	usermod -aG docker jenkins
  	echo "Added jenkins to the docker group"
  fi
else
  echo "docker group already exists"
fi

echo "export MASTER_SSH_PORT=$MASTER_SSH_PORT" >> "$JENKINS_HOME"/.bashrc
echo "export MASTER_SLAVE_PWD=$MASTER_SLAVE_PWD" >> "$JENKINS_HOME"/.bashrc
echo "export MASTER_SLAVE_USER=$MASTER_SLAVE_USER" >> "$JENKINS_HOME"/.bashrc

chown -R jenkins:jenkins "$JENKINS_HOME"

echo "Starting ssh daemon"
/usr/sbin/sshd -D