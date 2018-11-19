FROM python:2.7

MAINTAINER  Fernando Mendez Requena <fernando.mendez@atos.net>

RUN apt-get update && \
    apt-get -qq install -y \
    sudo libpq-dev postgresql postgresql-contrib -y -qq \
    sudo postgresql-client-common \
    dialog apt-utils \
    apache2 libapache2-mod-wsgi \
    python-pip \
    python-dev \
    python-virtualenv


ENV DIR_APACHE=../apache


RUN cd /etc/apache2/mods-available && \
    chmod 700 mpm_prefork.conf && \
    chmod 700 mpm_worker.conf && \
    echo "envsubst < $DIR_APACHE/mpm_prefork-template.conf > ./mpm_prefork.conf" \
    echo "envsubst < $DIR_APACHE/mpm_worker-template.conf > ./mpm_worker.conf"
    

RUN pip install --upgrade pip

#Show python errors
ENV PYTHONUNBUFFERED=1
ENV WEBAPP_DIR=/webapp/ShowcaseServer/

RUN mkdir /webapp && mkdir $WEBAPP_DIR

WORKDIR $WEBAPP_DIR

ADD requirements.txt $WEBAPP_DIR
RUN pip install -r requirements.txt
ADD manage.py $WEBAPP_DIR
ADD showcase_server $WEBAPP_DIR/showcase_server
ADD backend $WEBAPP_DIR/backend
ADD dashboard $WEBAPP_DIR/dashboard

ADD dev-setup.sh $WEBAPP_DIR
RUN cd $WEBAPP_DIR && \
    chmod 700 dev-setup.sh && \
    ./dev-setup.sh

EXPOSE 80

CMD apachectl -D FOREGROUND
