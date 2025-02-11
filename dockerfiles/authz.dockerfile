# Copyright (C) 2021 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

FROM python:3.6-slim-buster
LABEL maintainer Shivdeep Singh <shivdeep.singh@intel.com>

WORKDIR /app
COPY authz /app

RUN pip install -r /app/requirements.txt

# Install integration lib
COPY integration_library /tmp/integration_library
RUN cd /tmp/integration_library/zmq_integration_lib \
    && bash install.sh 

# Thin OBP client 
COPY nlp/obp_api /data/obp_api
RUN cd /data/obp_api \
    && pip install .

COPY dockerfiles/create_user.sh /create_user.sh
RUN chmod a+x /create_user.sh \
     && /create_user.sh \
     && rm /create_user.sh \
     && usermod -aG audio sys-admin
USER sys-admin
