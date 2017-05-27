## Docker container with certification rally tests inside.

### Quickstart.
`git clone https://github.com/pashkash/rally_docker_containers.git && cd ./rally_docker_containers/rally_cert && ./install.sh && docker run -v html_rally_reports:/home/rally/rally_arts/ -v ~/.ssh:/root/.ssh --net host -it pashkash/rally_certification`

On the last step we can build our own container instead of public and run it.
* `docker build --no-cache=true -t rally_certification .`
* `docker run -v html_rally_reports:/home/rally/rally_arts/ -v ~/.ssh:/root/.ssh --net host -it rally_certification`

Html reports will be stored in the `/var/lib/docker/volumes/html_rally_reports/` folder.
