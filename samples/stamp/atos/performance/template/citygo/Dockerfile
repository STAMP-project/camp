# See explanation in the README.

FROM camp/runtime

# Describe here how to install Citygo ontop of the "python" component.

ENV PYTHONUNBUFFERED 1
ENV C_FORCE_ROOT true

# Set work directory
WORKDIR /app 

RUN chmod -R +x /app
RUN pip install --upgrade pip

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

#copy entrypoint.sh
COPY ./entrypoint.sh /app/requirements.txt

# copy project
COPY . /app/

EXPOSE 8003

# run entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
