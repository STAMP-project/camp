FROM postgres:9.3

MAINTAINER  Fernando Mendez Requena <fernando.mendez.external@atos.net>

RUN apt-get update && apt-get install -my wget gnupg &&  apt-get install -y gettext-base


USER postgres

WORKDIR ./

ADD ./init-db.sql ./

RUN echo "/etc/init.d/postgresql start"
ADD ./postgresql.conf /etc/

RUN echo "psql -a -f init-db.sql"

RUN cd /etc && \
    echo "envsubst </etc/postgresql.conf > /var/lib/postgresql/data/postgresql.conf || cat /var/lib/postgresql/data/postgresql.conf"

EXPOSE 2345
