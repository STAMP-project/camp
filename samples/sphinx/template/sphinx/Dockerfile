FROM python:3.5-slim

RUN apt-get update && \
        #apt-get install -y --no-install-recommends imagemagick && \
        apt-get install -y imagemagick && \
        apt-get clean && \
        rm -rf /var/lib/apt/lists/*  

COPY ./src /sphinx
WORKDIR /sphinx

RUN pip3 install -e .[test]

CMD echo "Ready!"
