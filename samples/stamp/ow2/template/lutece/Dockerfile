#
# CAMP
#
# Copyright (C) 2017, 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#

ARG site=site-forms-demo-1.0.0-SNAPSHOT

# A first container to build the lutece web app
FROM debian:stretch as builder

LABEL stage="intermediate"

RUN apt-get update && apt-get dist-upgrade -y && \
        apt-get install -y --no-install-recommends \
        mysql-client \
        default-jdk \
        ant \
        maven \
        git

WORKDIR /app

ADD pom.xml /app/pom.xml

RUN mvn lutece:site-assembly

ADD db.properties /app/target/${site}/WEB-INF/conf/db.properties


# Deploy the web app on a Tomcat, which is installed in
# /usr/local/tomcat. See template/tomcat/Dockerfile
FROM camp/runtime

COPY --from=builder /app/target/${site}/ /usr/local/tomcat/webapps/site-forms-demo

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["sh", "/entrypoint.sh"]
