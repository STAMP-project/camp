# Installation of Python 2.7

# Replaced by CAMP during realization
FROM camp/runtime

RUN apt-get update \
    && apt-get install -y --no-install-recommends python2.7 \
    && rm -rf  /usr/bin/python \
    && ln -s /usr/bin/python2.7 /usr/bin/python 
