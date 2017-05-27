FROM rallyforge/rally:0.7.0

LABEL description="Contains rally test tool \
with longevity rally test plugins and scenarios"

USER root 

VOLUME ["html_rally_reports"]

ADD ./rally_plugins/ ./rally_plugins/
ADD ./rally_tests/ ./rally_tests/
ADD ./resources/ ./resources/
ADD ./run_rally.sh ./rally.conf ./Makefile ./


ENV OS_USERNAME=admin
ENV OS_PASSWORD=password
ENV OS_TENANT_NAME=admin
ENV OS_AUTH_URL=http://10.167.4.10:35357/v2.0
ENV OS_REGION_NAME=RegionOne
ENV OS_SERVICE_TOKEN=password
ENV OS_SERVICE_ENDPOINT="http://10.167.4.10:35357/v2.0/"
ENV OS_ENDPOINT_TYPE="internal"
ENV OS_CACERT="./resources/ca-certificates.crt"
ENV JOB_PARAMS_CONFIG /home/rally/rally.conf

# whole test suit
ENV SCENARIOS_DIR ./rally_tests

ENV ARTIFACTS_DIR /home/rally/rally_arts
RUN mkdir $ARTIFACTS_DIR

ENV PLUGINS_PATH /opt/rally/plugins
RUN mkdir $PLUGINS_PATH
RUN cp -r ./rally_plugins/* $PLUGINS_PATH

CMD apt-get install make; \
	glance image-create --name ubuntu_14.04 --disk-format raw --container-format bare --visibility public --file "./resources/trusty-server-cloudimg-amd64-disk1.img"; \
	neutron net-update admin_internal_net --shared true; \
	openstack quota set --ram 102400 admin; \
	make test;
