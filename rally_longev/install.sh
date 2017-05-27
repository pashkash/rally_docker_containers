#!/bin/bash
# This file create necessary files for working langevitydocker container.

#1. download image with ubuntu
wget -P ./resources/ https://cloud-images.ubuntu.com/trusty/current/trusty-server-cloudimg-amd64-disk1.img 

#2. copy cert file
cp /etc/ssl/certs/ca-certificates.crt ./resources/

#3. make&store node config file
HOME_CONFIG="$(pwd)/resources/rackspacetruck.cfg"

echo "[nodes]" > "${HOME_CONFIG}"
for i in $(salt-run manage.status | grep " - " | grep "cmp\|ctl" | awk -F  " - " '{print $2}'); do
  IFS='.' read -r -a str <<< ${i}
  number=${str[0]:3}
  case "${i}" in
    *"ctl"*)
        echo "controller_$((number+0)) = ${i}" >> "${HOME_CONFIG}"
        ;;
    *"cmp"*)
        echo "compute_$((number+0)) = ${i}" >> "${HOME_CONFIG}"
        ;;
  esac
done

#4. now we can run container from public repo (or we can build it with "docker build --no-cache=true -t longevity .")
#docker run -v html_reports:/home/rally/rally_arts/ \
#    -v $PWD/resources/:/home/rally/resources/ \
#    -v ~/.ssh:/root/.ssh \
#    -e OS_AUTH_URL=http://10.167.4.10:35357/v2.0 \
#    --net host \
#    -it pashkash/longevity