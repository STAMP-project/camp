FROM postgres:9.3

MAINTAINER  Fernando Mendez Requena <fernando.mendez.external@atos.net>

RUN apt-get update && \
    apt-get install -my wget gnupg &&  apt-get install -y gettext-base

USER postgres

ENV DIR_DB=/etc
RUN mkdir $DIR_DB
WORKDIR $DIR_DB

ADD init-db.sql $DIR_DB

RUN /etc/init.d/postgresql start && \
    psql -a -f init-db.sql && \
    /etc/init.d/postgresql stop
    
ADD postgresql.conf /etc/

RUN cd /var/lib/postgresql/data/postgresql.conf && \
    chmod 700 postgresql.conf && \
    envsubst < $DIR_DB/postgresql.conf > ./postgresql.conf
    
EXPOSE $port

# Set the default command to run when starting the container
CMD ["/usr/bin/postgresql", "-D", "/var/lib/postgresql/data", "-c", "config_file=/var/lib/postgresql/data/postgresql.conf"]
