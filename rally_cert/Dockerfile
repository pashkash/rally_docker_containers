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
ENV OS_CACERT="./resources/ca-certificates.crt"
ENV ARTIFACTS_DIR /home/rally/rally_arts
ENV SCENARIOS_DIR ./rally_scenarios

RUN mkdir $PLUGINS_PATH
RUN mkdir $ARTIFACTS_DIR

ADD ./rally_plugins/ $PLUGINS_PATH
ADD ./rally_scenarios/ $SCENARIOS_DIR
#ADD ./run_rally.sh ./rally.conf ./ca-certificates.crt ./Makefile ./
ADD ./run_rally.sh ./rally.conf ./Makefile ./


#RUN cp -r ./mos-scale/deploy/deploy_tests/deploy_rally/deploy_rally/rally_plugins/* $PLUGINS_PATH

CMD apt-get install make; make test;


# command: docker run -v html_rally_reports:/home/rally/rally_arts/ -v ~/.ssh:/root/.ssh --net host -it perf-rally 
# explain: reports will be stored here /var/lib/docker/volumes









# RUN rally-manage db recreate
# RUN rally deployment create --fromenv --name=Current

# CMD rally-manage db recreate;rally deployment create --fromenv --name=Current;rally --debug task start /var/rally-scenarios/cinder/create-and-attach-volume.yaml --task-args '{"compute": "1", "concurrency":"1"}'
# CMD rally-manage db recreate;rally deployment create --fromenv --name=Current;rally --debug task start /var/rally-scenarios/keystone/get_entities.yaml --task-args '{"compute": "1", "concurrency":"1"}'



#rally-manage db recreate;rally deployment create --fromenv --name=Current;rally --debug task start ./mos-scenarios/rally-scenarios/keystone/get_entities.yaml --task-args '{"compute": "1", "concurrency":"1"}'

###
# docker volume create --name=html_reports 
## now we have /var/lib/docker/volumes/html_reports
# docker run -v html_reports:/home/rally/rally_arts/ --net host -it perf-rally /bin/bash
## here is data: docker volume inspect html_reports



# 
# docker run --net host -it perf-rally /bin/bash
# docker run -v ~/rally-arts:/home/rally/rally-arts/ --net host -it perf-rally /bin/bash
# docker run -v ~/mos-scenarios:/var/ -v ~/.ssh:/root/.ssh --net host -it perf-rally /bin/bash
# docker run -v ~/mos-scenarios:/var/ -v ~/.ssh:/root/.ssh --net host -it perf-rally 
# docker build --no-cache=true -t perf-rally .

# rally task report --tasks dd67f4e4-dc79-4988-bf94-f3f5e20f8a38 --html-static --out /home/rally/rally-arts/rally_report.html


# CMD ["make", "test"]



#RUN rally deployment create --file=/mos-scenarios/existing.json --name=existing

#EXPOSE 29418
#RUN git clone http://pshvetsov:A6f36JitW0SkNcAdLiXRwnLTry7uJtRVYQMfXF8P9g@gerrit.mirantis.com/a/mos-scale/mos-scenarios
#RUN git clone http://pshvetsov:A6f36JitW0SkNcAdLiXRwnLTry7uJtRVYQMfXF8P9g@gerrit.mirantis.com/a/mos-scale/mos-scale

#RUN mkdir ~/mos-scenarios
#COPY ~/mos-scenarios ~/mos-scenarios/

#RUN rally --debug task start ~/mos-scenarios/rally-scenarios/keystone/get_entities.yaml --task-args '{"compute": "1", "concurrency":"1"}'

# Remove all running containers
# docker rm --force $(docker ps -aq)

# docker build --no-cache=true -t perf-rally .


# RUN pip install -U -r ./mos-scale/requirements.txt
# ENV HTTP_PROXY=http://${CONTROLLER_HOST}:8888
# ENV HTTPS_PROXY=http://${CONTROLLER_HOST}:8888






#docker run -v html_rally_reports:/home/rally/rally_arts/ --net host -it pashkash/rally_certification
#docker run -v html_rally_reports:/home/rally/rally_arts/ --net host -it perf-rally