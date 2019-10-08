FROM selenium/node-chrome-debug

RUN sudo apt-get update && \
    sudo apt-get upgrade -y && \
    sudo apt-get install -y \
    python2.7 \
    python-pip

WORKDIR ./

RUN pip install --upgrade pip

ADD ./requirements.txt ./
RUN pip install -r requirements.txt

COPY ./tests.py citygo-tests/tests.py

CMD echo "Ready!"
