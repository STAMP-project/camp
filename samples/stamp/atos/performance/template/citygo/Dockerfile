# See explanation in the README.

FROM camp/runtime


# Describe here how to install Citygo ontop of the "python" component.

ENV PYTHONUNBUFFERED 1
ENV C_FORCE_ROOT true

# Set work directory
WORKDIR /usr/src/app

RUN chmod -R +x /usr/src/app

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

#copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# copy project
COPY . /usr/src/app/

EXPOSE 8000

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

