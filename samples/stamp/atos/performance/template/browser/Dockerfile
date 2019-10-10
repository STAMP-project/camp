FROM selenium/node-chrome-debug

RUN sudo apt-get update && \
    sudo apt-get upgrade -y && \
    sudo apt-get install -y \
    python2.7 \
    python-pip

WORKDIR ./browser

RUN pip install --upgrade pip

RUN sudo -H pip install bzt

COPY ./citygo.jmx /browser/citygo-tests/citygo.jmx

CMD echo "Ready!"
