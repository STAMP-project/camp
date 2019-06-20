#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


FROM python:3.7-slim-stretch

RUN apt-get update && \
        apt-get install -y --no-install-recommends git=1:2.11.0-3+deb9u4 && \
        apt-get clean && \
        rm -fr /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY . /tests

WORKDIR /tests

RUN pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org .

CMD green --junit-report
