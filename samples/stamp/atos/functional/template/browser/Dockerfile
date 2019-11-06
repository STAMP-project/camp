FROM selenium/node-chrome-debug

RUN sudo apt-get update && \
    sudo apt-get upgrade -y && \
    sudo apt-get install -y \
    python3 \
    python3-pip

WORKDIR /browser

USER root
RUN chmod 777 -R /browser

#Install requirements.txt
COPY ./requirements.txt /browser/
RUN sudo -H pip3 install -r requirements.txt

#Funtional Tests
COPY ./tests.py /browser/citygo-tests/tests.py

RUN ls -lR /browser

CMD echo "Ready!"
