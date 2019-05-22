#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#

FROM debian:9-slim


ARG DEBUG
ARG PYTHON_VERSION=3.5
ARG WITH_TESTS
ARG Z3_VERSION=4.8.4.d6df51951f4c
ARG Z3_PLATFORM=x64-debian-8.11

LABEL maintainer "franck.chauvel@sintef.no"


WORKDIR /camp
COPY . /camp

# Install Z3
RUN bash install.sh \
        --install-python \
        --python-version ${PYTHON_VERSION} \
        --install-z3 \
        --z3-version ${Z3_VERSION} \
        --z3-platform ${Z3_PLATFORM} \
        --install-docker \
        --camp-from-sources ${WITH_TESTS} ${DEBUG}

# Avoid UnicodeDecodeError as per Issue #53
ENV LANG C.UTF-8
