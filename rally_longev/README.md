## Docker container with longevity rally tests inside. 

### Quickstart.
`git clone https://github.com/pashkash/rally_docker_containers.git & cd rally_longev & ./install.sh & docker run -v html_reports:/home/rally/rally_arts/ -v $PWD/resources/:/home/rally/resources/ -e OS_AUTH_URL=http://10.167.4.10:35357/v2.0 -e OS_SERVICE_ENDPOINT=http://10.167.4.10:35357/v2.0/ --net host -it pashkash/longevity`

On the last step we can build our own container instead of public and run it.
* `docker build --no-cache=true -t longevity .`
* `docker run -v html_rally_reports:/home/rally/rally_arts/ -v $PWD/resources/:/home/rally/resources/ -e OS_AUTH_URL=http://10.167.4.10:35357/v2.0 -e OS_SERVICE_ENDPOINT=http://10.167.4.10:35357/v2.0/ --net host -it longevity`

Html reports will be stored in the `/var/lib/docker/volumes/html_rally_reports/` folder.
