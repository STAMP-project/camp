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

LABEL maintainer "franck.chauvel@sintef.no"


WORKDIR /camp
COPY . /camp

# Install Z3
RUN bash install.sh --install-z3 --install-docker --camp-from-sources
        
