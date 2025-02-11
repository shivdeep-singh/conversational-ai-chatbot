# Copyright (C) 2021 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

FROM python:3.6-slim-buster
LABEL maintainer Shivdeep Singh <shivdeep.singh@intel.com>


WORKDIR /app
# copy the content of the local src directory to the working directory
COPY nlp/app/* /app/
# Installing requirements 
RUN python3 -mpip install -r /app/requirements.txt

# Install integration lib
COPY integration_library /tmp/integration_library
RUN cd /tmp/integration_library/zmq_integration_lib \
    && bash install.sh 

COPY dockerfiles/create_user.sh /create_user.sh
RUN chmod a+x /create_user.sh \
     && /create_user.sh \
     && rm /create_user.sh \
     && usermod -aG audio sys-admin
USER sys-admin
