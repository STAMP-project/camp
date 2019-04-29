FROM ubuntu

MAINTAINER  Fernando Mendez Requena <fernando.mendez@atos.net>

RUN apt-get update && \
    apt-get install -y \
    apache2 \
    python-pip \
    python2.7 \
    libapache2-mod-wsgi \
    lynx

RUN pip install virtualenv
ADD ./requirements.txt ./
RUN pip install -r requirements.txt

WORKDIR ./

ADD ./mpm_event.conf ./

ADD ./demo_site.conf /etc/apache2/sites-available/000-default.conf


CMD service apache2 reload

#Setting permission to allow Citygo app write logs
RUN chmod 777 -R /var/log/apache2/

RUN cd /etc/apache2/mods-enabled/ && \
    echo "envsubst < $pwd/mpm_event.conf > ./mpm_event.conf"


EXPOSE 80 3500

CMD ["apache2ctl", "-D", "FOREGROUND"]

#ENTRYPOINT ["/docker-entrypoint.sh"]
