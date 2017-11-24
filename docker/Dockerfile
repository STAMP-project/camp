FROM buildpack-deps:jessie

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        unzip \
        python-dev \
        python-pip \
        && \
    apt-get install --reinstall python-pkg-resources && \
    rm -rf /var/lib/apt/lists/* &&\
    pip install PyYAML

WORKDIR /root
RUN wget https://github.com/Z3Prover/z3/releases/download/z3-4.5.0/z3-4.5.0-x64-debian-8.5.zip && \
    unzip z3-4.5.0-x64-debian-8.5.zip && \
    mkdir /root/z3-4.5.0-x64-debian-8.5/bin/python/z3/lib && \
    cp /root/z3-4.5.0-x64-debian-8.5/bin/lib* /root/z3-4.5.0-x64-debian-8.5/bin/python/z3/lib/ && \
    cp /root/z3-4.5.0-x64-debian-8.5/bin/z3 /root/z3-4.5.0-x64-debian-8.5/bin/python/z3/lib/ && \
    cp -rf /root/z3-4.5.0-x64-debian-8.5/bin/python/z3 /usr/lib/python2.7/ && \
    rm -rf *    

WORKDIR /root
RUN git clone -b multi-root https://github.com/SINTEF-9012/ozepy && \
    git clone -b metamodel-sintef https://songhui@gitlab.ow2.org/stamp/conf-test-ampli.git && \
    pip install -r conf-test-ampli/dockergen/requirements.txt

COPY start.sh /root/start.sh

ENV PYTHONPATH=/root/ozepy
CMD ["/bin/bash", "./start.sh"]

