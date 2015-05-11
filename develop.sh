#! /bin/bash
mongod &
virtualenv --no-site-packages .
source bin/activate
pip install -r config/requirements.txt
consul agent \
    -server \
    -bootstrap \
    -client 0.0.0.0 \
    -data-dir data/consul_data \
    -ui-dir /usr/share/consul/ui > log/consul.log &
config/setup_consul_dev.sh
