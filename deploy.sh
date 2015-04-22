#! /bin/bash

NGINX_CONFIG=/etc/nginx/sites-available/adi-website
ADI_WWWW=/srv/adi-website/www
DOCKERFILE=Dockerfile
PORT1=7000
PORT2=6000
NAME1="adi-website-1"
NAME2="adi-website-2"


if [ ! -e "$NGINX_CONFIG" ]; then
    echo "Cannot find file $NGINX_CONFIG. Are you running this on the server?"
    exit
fi

# Swap the port in nginx and in the Dockerfile
PORT="$(cat $NGINX_CONFIG | grep 'set \$ADI_WEBSITE_PORT' | grep -o '[0-9]*')"
if [ $PORT -eq $PORT1 ]; then
    sed -i "s/$PORT1/$PORT2/g" $NGINX_CONFIG
    sed -i "s/$PORT1/$PORT2/g" $DOCKERFILE
elif [ $PORT -eq $PORT2 ]; then
    sed -i "s/$PORT2/$PORT1/g" $NGINX_CONFIG
    sed -i "s/$PORT2/$PORT1/g" $DOCKERFILE
else
    echo "adi-website running on unknown port: $PORT"
    exit
fi

# Validate nginx configurations
if [ ! nginx -t ]; then
    echo "Nginx config failed!"
    exit
fi

# Determine the new and old container names
NEW_NAME=""
OLD_NAME=""
CURRENT_NAME="$(docker ps -a | grep adi-website | awk 'NF>1{print $NF}')"
if [ "$CURRENT_NAME" == "$NAME1" ]; then
    OLD_NAME=$NAME1
    NEW_NAME=$NAME2
elif [ "$CURRENT_NAME" == "$NAME2" ]; then
    OLD_NAME=$NAME2
    NEW_NAME=$NAME1
else
    echo "Docker Image has unknown name $CURRENT_NAME"
    exit
fi

# Startup the new container
docker build -t $NEW_NAME .
docker run \
    --net=host \
    -v $ADI_WWW/../logs:/opt/logs \
    -v $ADI_WWW/app/static/img/uploaded:/app/static/img/uploaded \
    -d \
    --name="$NEW_NAME" $NEW_NAME

# swap to the new container
sudo service nginx restart

# Kill the old container
docker kill $OLD_NAME
docker rm $OLD_NAME
