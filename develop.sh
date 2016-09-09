#! /bin/bash
mongod &
virtualenv --no-site-packages venv
source venv/bin/activate
pip install -r config/requirements.txt
source config/secrets.dev
