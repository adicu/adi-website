#! /bin/bash

ADI_WWWW=/srv/adi-website/www
DOCKERFILE=Dockerfile
NAME="adi-website"

# Kill the old container
docker kill $NAME
docker rm $NAME

# Startup the new container
docker build -t $NAME .

# --net: Use the local network stack
# --restart: Always restart, even if it crashes
# -v: mount a volume, to ensure that edited log files live on the server,
#     not in the docker box.
# --volumes-from: Mount the uploaded images filesystem, so that new image
#                 live on the server, not in the docker box.
# -d: detach after running, instead of entering the container
# --name: Set the name of the container

docker run \
    --net=host \
    --restart=always \
    -v $ADI_WWWW/../logs:/logs \
    -v $ADI_WWWW/app/static/img/uploaded:/app/static/img/uploaded \
    -d \
    --name="$NAME" $NAME
