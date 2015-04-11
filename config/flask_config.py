from os import environ, path, pardir
from sys import exit
import json

# dictionary the flask app configures itself from
config = {
    'HOST': '0.0.0.0',
    'PORT': None,
    'SECRET_KEY': None,
    'INSTALLED_APP_CREDENTIALS_PATH': None,
    'CREDENTIALS_PATH': None,
    'GOOGLE_AUTH_ENABLED': None,
    'CLIENT_SECRETS_PATH': None,
    'CSRF_ENABLED': None,
    'CSRF_SESSION_KEY': None,
    'DEBUG': False,
    'PRIVATE_CALENDAR_ID': None,
    'PUBLIC_CALENDAR_ID': None,
    'MONGO_DATABASE': None,
    'LOG_FILE_MAX_SIZE': None,
    'APP_LOG_NAME': None,
    'WERKZEUG_LOG_NAME': None
}

# consul_configurations contains equivalent keys that will be used to extract
# configuration values from Consul.
consul_configurations = [  # consul key --> config key
    ('flask_port', 'PORT'),
    ('flask_debug', 'DEBUG'),
    ('secret_key', 'SECRET_KEY'),
    ('installed_app_client_secret_path', 'INSTALLED_APP_CLIENT_SECRET_PATH'),
    ('installed_app_credentials_path', 'INSTALLED_APP_CREDENTIALS_PATH'),
    ('google_auth_enabled', 'GOOGLE_AUTH_ENABLED'),
    ('client_secrets_path', 'CLIENT_SECRETS_PATH'),
    ('csrf_enabled', 'CSRF_ENABLED'),
    ('csrf_session_key', 'CSRF_SESSION_KEY'),
    ('private_calendar_id', 'PRIVATE_CALENDAR_ID'),
    ('public_calendar_id', 'PUBLIC_CALENDAR_ID'),
    ('mongo_database', 'MONGO_DATABASE'),
    ('log_file_max_size', 'LOG_FILE_MAX_SIZE'),
    ('app_log_name', 'APP_LOG_NAME'),
    ('werkzeug_log_name', 'WERKZEUG_LOG_NAME')
]

# config variables that must be set for the app to work
critical_config_vars = [
    'SECRET_KEY',
    'GOOGLE_AUTH_ENABLED',
    'CSRF_ENABLED',
    'CSRF_SESSION_KEY',
    'PRIVATE_CALENDAR_ID',
    'PUBLIC_CALENDAR_ID'
]

if environ.get('USE_ENV_VARS') == 'TRUE':  # use env variables
    for env_key, value in config.iteritems():
        if not value:
            config[env_key] = environ.get(env_key)
else:
    from consul import Consul
    kv = Consul().kv  # initalize client to KV store

    # get values from Consul and set the corresponding config variable to the
    # value retrieved from Consul.
    for consul_key, config_key in consul_configurations:
        _, consul_value = kv.get("adi-website/{}".format(consul_key))
        val = consul_value.get('Value')
        config[config_key] = val
        if not val:
            raise Exception(("No value found in Consul for key "
                             "adi-website/{}").format(consul_key))


# make sure critical config variables are set
for config_var in critical_config_vars:
    if config[config_var] is None or config[config_var] == '':
        raise Exception("Critical config variable {} has not been "
                        "set".format(config_var))

# basic flask settings
config['PORT'] = int(config['PORT'])

# Google Auth
# This is used for the webapp that allows Google+ login
config['GOOGLE_AUTH_ENABLED'] = True if config['GOOGLE_AUTH_ENABLED'] == 'TRUE' \
                                else False

# Setup Google Auth
if config['GOOGLE_AUTH_ENABLED']:
    try:
        with open(config['CLIENT_SECRETS_PATH'], 'r') as f:
            _secrets_data = json.loads(f.read())['web']
            config['GOOGLE_CLIENT_ID'] = _secrets_data['client_id']
            if not _secrets_data.get('client_secret', None):
                print ('Google Auth config file, %s,'
                       ' missing client secret', config['CLIENT_SECRETS_PATH'])
                exit(1)

    except IOError:
        print ("The Google client_secrets file was not found at '{}', "
               "check that it exists.".format(config['CLIENT_SECRETS_PATH']))
        exit(1)

# Cross-site request forgery settings
config['CSRF_ENABLED'] = True if config['CSRF_ENABLED'] == 'TRUE' else False

# Mongo configs
config['MONGODB_SETTINGS'] = {'DB': config['MONGO_DATABASE']}

############################################################################
#  Constants in version control
############################################################################

# Base directory
config['BASEDIR'] = path.abspath(path.join(path.dirname(__file__), pardir))

config['RELATIVE_UPLOAD_FOLDER'] = 'app/static/img/uploaded/'
config['UPLOAD_FOLDER'] = path.join(config['BASEDIR'], config['RELATIVE_UPLOAD_FOLDER'])
config['RELATIVE_DELETE_FOLDER'] = 'app/static/img/uploaded/deleted/'
config['DELETE_FOLDER'] = path.join(config['BASEDIR'], config['RELATIVE_DELETE_FOLDER'])

# The file extensions that may be uploaded
config['ALLOWED_UPLOAD_EXTENSIONS'] = set(['.txt',
    '.pdf',
    '.png',
    '.jpg',
    '.jpeg',
    '.gif'
])

config['DEVFEST_BANNER'] = False
