#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#

# Deploy the WAR file into a Tomcat instance
FROM tomcat:8-jre8

COPY target/testman-0.1.0.BUILD-SNAPSHOT.war /usr/local/tomcat/webapps/testman.war

CMD ["catalina.sh", "run"]
