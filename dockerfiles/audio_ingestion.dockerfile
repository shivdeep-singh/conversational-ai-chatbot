# Copyright (C) 2021 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

FROM ubuntu:18.04
LABEL maintainer Shivdeep Singh <shivdeep.singh@intel.com>

RUN mkdir -p /app
COPY audio_ingestion/requirements.txt /app/

RUN apt update -y \
    && apt install -y python3-pip
RUN pip3 install -r /app/requirements.txt

COPY audio_ingestion/src /app/src

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

CMD ["python3", "/app/src/main.py"]
