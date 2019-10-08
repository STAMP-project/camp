# See explanation in the README.

FROM camp/runtime

# Describe here how to install Citygo ontop of the "python" component.

ENV PYTHONUNBUFFERED 1
ENV C_FORCE_ROOT true

# Set work directory
WORKDIR ./ 

#RUN chmod -R +x /usr/src/app
RUN pip install --upgrade pip

ADD ./requirements.txt ./
RUN pip install -r requirements.txt

#copy entrypoint.sh
COPY ./entrypoint.sh ./

# copy project
COPY . ./

EXPOSE 8003

# run entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
