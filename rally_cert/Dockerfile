FROM rallyforge/rally:0.7.0

LABEL description="Contains rally test tool \
with standard rally test scenarios"

USER root 

VOLUME ["html_rally_reports"]

ENV PLUGINS_PATH /opt/rally/plugins
ENV OS_NO_CACHE='true'
ENV OS_TENANT_NAME='admin'
ENV OS_PROJECT_NAME='admin'
ENV OS_USERNAME='admin'
ENV OS_PASSWORD='password'
ENV OS_AUTH_URL=http://10.167.4.10:35357/v2.0
ENV OS_DEFAULT_DOMAIN='Default'
ENV OS_AUTH_STRATEGY='keystone'
ENV OS_REGION_NAME='RegionOne'
ENV OS_SERVICE_TOKEN=password
ENV OS_SERVICE_ENDPOINT="http://10.167.4.10:35357/v2.0/"
ENV OS_ENDPOINT_TYPE='internal'
ENV JOB_PARAMS_CONFIG /home/rally/rally.conf
ENV OS_CACERT="./ca-certificates.crt"
ENV ARTIFACTS_DIR /home/rally/rally_arts
ENV SCENARIOS_DIR ./rally_scenarios

RUN mkdir $PLUGINS_PATH
RUN mkdir $ARTIFACTS_DIR

ADD ./rally_plugins/ $PLUGINS_PATH
ADD ./rally_scenarios/ $SCENARIOS_DIR
ADD ./run_rally.sh ./rally.conf ./Makefile ./

CMD apt-get install make; make test;
