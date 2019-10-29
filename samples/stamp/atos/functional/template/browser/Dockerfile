FROM selenium/node-chrome-debug

RUN sudo apt-get update && \
    sudo apt-get upgrade -y && \
    sudo apt-get install -y \
    python2.7 \
    python-pip

WORKDIR /browser

USER root
RUN chmod 777 -R /browser

RUN pip install --upgrade pip

# Install BlazeMetter to run performance Tests
RUN sudo -H pip install bzt
COPY ./citygo.jmx /browser/citygo-tests/citygo.jmx

#Funtional Tests
COPY ./tests.py /browser/citygo-tests/citygo.jmx/tests.py

RUN ls -lR /browser

CMD echo "Ready!"
