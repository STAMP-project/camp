FROM ubuntu

MAINTAINER  Fernando Mendez Requena <fernando.mendez@atos.net>

#Updated line to solve while testing CAMP
RUN apt-get update && apt-get install -my wget gnupg

# Add the PostgreSQL PGP key to verify their Debian packages.
# It should be the same key as https://www.postgresql.org/media/keys/ACCC4CF8.asc
RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8

# Add PostgreSQL's repository. It contains the most recent stable release
#     of PostgreSQL, ``9.3``.
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" > /etc/apt/sources.list.d/pgdg.list

# Install ``python-software-properties``, ``software-properties-common`` and PostgreSQL 9.3
#  There are some warnings (in red) that show up during the build. You can hide
#  them by prefixing each apt-get statement with DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y python-software-properties software-properties-common postgresql-9.3 postgresql-client-9.3 postgresql-contrib-9.3 gedit

# Adjust PostgreSQL configuration so that remote connections to the
# database are possible.
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.3/main/pg_hba.conf

# And add ``listen_addresses`` to ``/etc/postgresql/9.3/main/postgresql.conf``
RUN echo "listen_addresses='*'" >> /etc/postgresql/9.3/main/postgresql.conf

ENV DIR_DB=/db
RUN mkdir $DIR_DB
WORKDIR $DIR_DB

USER postgres
ADD init-db.sql $DIR_DB

RUN service postgresql start && \
    psql -a -f init-db.sql && \
    service postgresql stop

ADD postgresql-template.conf $DIR_DB

RUN cd /etc/postgresql/9.3/main && \
    chmod 700 postgresql.conf && \  
    echo "envsubst < $DIR_DB/postgresql-template.conf > ./postgresql.conf"
   
#WORKDIR /docker-entrypoint-initdb.d/
#ADD init-db.sql /docker-entrypoint-initdb.d

EXPOSE 5432

#COPY start.sh /$DIR_DB/start.sh

#CMD $DIR_DB/start.sh

# Set the default command to run when starting the container
CMD ["/usr/lib/postgresql/9.3/bin/postgres", "-D", "/var/lib/postgresql/9.3/main", "-c", "config_file=/etc/postgresql/9.3/main/postgresql.conf"]
