#! /bin/bash

./consul agent -server -bootstrap-expect 1 -data-dir /tmp/consul &
sleep 10  # sleep while it starts up
./config/setup_consul_travis.sh
curl http://localhost:8500/v1/kv/adi-website\?recurse
nosetests
