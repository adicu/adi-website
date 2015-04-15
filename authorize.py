import argparse
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run_flow
from oauth2client import tools

from config import flask_config

parser = argparse.ArgumentParser(parents=[tools.argparser])
FLAGS = parser.parse_args()
SCOPE = 'https://www.googleapis.com/auth/calendar'

FLOW = flow_from_clientsecrets(flask_config.INSTALLED_APP_SECRET_PATH,
                               scope=SCOPE)

# Save the credentials file here for use by the app
storage = Storage(flask_config.INSTALLED_APP_CREDENTIALS_PATH)
run_flow(FLOW, storage, FLAGS)
