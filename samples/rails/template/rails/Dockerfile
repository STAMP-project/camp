#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


FROM ruby:2.6.3-stretch
#NOTE: PostgreSQL installation fails on ruby:2.6.3-slim-stretch

LABEL maintainer "franck.chauvel@sintef.no"

COPY rails /opt/rails
COPY setup_services.sh /opt/rails/setup_services.sh
COPY run_tests.sh /opt/rails/run_tests.sh

WORKDIR /opt/rails

RUN bash setup_services.sh

ENV LANG C.UTF-8


