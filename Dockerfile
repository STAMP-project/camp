FROM debian:8.11-slim

LABEL maintainer "franck.chauvel@sintef.no"

RUN apt-get update && \
    apt-get install -y --no-install-recommends  \
	libgomp1=4.9.2-10+deb8u2 \
	python2.7-dev=2.7.9-2+deb8u2 \
	python-pip=1.5.6-5 \
	wget=1.16-1+deb8u5 \
	unzip=6.0-16+deb8u3 \
	git=1:2.1.4-2.1+deb8u7 \
	&& \
    apt-get install -y --no-install-recommends --reinstall \
	python-pkg-resources=5.5.1-1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /root
RUN wget -q https://github.com/Z3Prover/z3/releases/download/z3-4.7.1/z3-4.7.1-x64-debian-8.10.zip && \
    unzip z3-4.7.1-x64-debian-8.10.zip && \
    mv z3-4.7.1-x64-debian-8.10 unzipped && \
    mkdir -p /usr/lib/python2.7/z3/lib && \
    cp unzipped/bin/z3 /usr/lib/python2.7/z3/lib/  && \
    cp unzipped/bin/lib* /usr/lib/python2.7/z3/lib/ && \
    cp -rf unzipped/bin/python/z3 /usr/lib/python2.7/ && \
    ln -s /usr/lib/python2.7/z3/lib/z3 /usr/bin/z3 && \
    rm -rf unzipped

RUN env && python -c 'import z3; print(z3.get_version_string())'

WORKDIR /camp
COPY . /camp
RUN pip install -r requirements.txt && \
    pip install .
