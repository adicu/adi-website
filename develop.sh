#! /bin/bash
mongod &
virtualenv --no-site-packages .
source bin/activate
pip install -r config/requirements.txt
consul agent \
    -server \
    -bootstrap \
    -advertise 127.0.0.1 \
    -client 127.0.0.1 \
    -data-dir data/consul_data \
    -ui-dir /usr/share/consul/ui > log/consul.log &
