# See explanation in the README.

FROM camp/runtime
# Describe here how to install Citygo ontop of the "python" component.

ENV PYTHONUNBUFFERED 1
ENV C_FORCE_ROOT true

# Set work directory
WORKDIR /usr/src/app

RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

#copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/

RUN chmod +x /usr/src/app/entrypoint.sh
# copy project
COPY . /usr/src/app/
RUN chmod -R 777 /usr/src/app

EXPOSE 82

# run entrypoint.sh
ENTRYPOINT ["/bin/sh","/usr/src/app/entrypoint.sh"]
