FROM buildpack-deps:jessie

LABEL maintainer "franck.chauvel@sintef.no"

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        unzip \
        python-dev \
        python-pip \
        && \
    apt-get install --reinstall python-pkg-resources && \
    rm -rf /var/lib/apt/lists/* 

WORKDIR /root
RUN wget https://github.com/Z3Prover/z3/releases/download/z3-4.5.0/z3-4.5.0-x64-debian-8.5.zip && \
    unzip z3-4.5.0-x64-debian-8.5.zip && \
    mkdir /root/z3-4.5.0-x64-debian-8.5/bin/python/z3/lib && \
    cp /root/z3-4.5.0-x64-debian-8.5/bin/lib* /root/z3-4.5.0-x64-debian-8.5/bin/python/z3/lib/ && \
    cp /root/z3-4.5.0-x64-debian-8.5/bin/z3 /root/z3-4.5.0-x64-debian-8.5/bin/python/z3/lib/ && \
    cp -rf /root/z3-4.5.0-x64-debian-8.5/bin/python/z3 /usr/lib/python2.7/ && \
    rm -rf *    

WORKDIR /camp
COPY . /camp
RUN pip install -r requirements.txt && \
    pip install .
    

