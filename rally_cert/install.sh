#!/bin/bash
# This file create necessary files for working langevitydocker container.

#1. copy cert file
cp /etc/ssl/certs/ca-certificates.crt ./resources/

#2. now we can run container from public repo (or we can build it with "docker build --no-cache=true -t rally_certification .")
#docker run -v html_reports:/home/rally/rally_arts/ \
#    -v $PWD/resources/:/home/rally/resources/ \
#    -v ~/.ssh:/root/.ssh \
#    -e OS_AUTH_URL=http://10.167.4.10:35357/v2.0 \
#    --net host \
#    -it pashkash/rally_certification