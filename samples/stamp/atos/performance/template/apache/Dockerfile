FROM httpd:2.4

MAINTAINER  Fernando Mendez Requena <fernando.mendez@atos.net>

RUN echo "sudo usermod -a -G user apache"

RUN apt-get update -y  && \
    apt-get upgrade -y && \
    apt-get install -y \
    libapache2-mod-wsgi \
    libxml2-dev \
    python-psycopg2 \
    python2.7 \
    python-pip \
    lynx \
    apache2

RUN pip install mod_wsgi
RUN pip install  virtualenv
ADD ./requirements.txt ./
RUN pip install -r requirements.txt

WORKDIR ./

ADD ./mpm_event.conf ./
ADD ./demo_site_1.conf /etc/apache2/sites-available/000-default.conf
ADD ./httpd.conf /usr/local/apache2/conf/httpd.conf


RUN chmod 777 -R /var/log/apache2
RUN cd /etc/apache2/mods-enabled/ && \
    echo "envsubst < $pwd/mpm_event.conf > ./mpm_event.conf"

CMD service apache2 restart

EXPOSE 80 3500

CMD ["apache2ctl", "-D", "FOREGROUND"]
