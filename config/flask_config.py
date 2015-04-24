from os import environ, path, pardir
from sys import exit
import json

# dictionary the flask app configures itself from
# several variables initialized to defaults
config = {
    'HOST': 'localhost',
    'PORT': 5000,
    'INSTALLED_APP_CLIENT_SECRET_PATH': 'client_secrets.json',
    'INSTALLED_APP_CREDENTIALS_PATH': 'config/credentials.json',
    'CLIENT_SECRETS_PATH': 'config/client_secrets.json',
    'MONGO_DATABASE': 'eventum',
    'LOG_FILE_MAX_SIZE': '256',
    'APP_LOG_NAME': 'app.log',
    'WERKZEUG_LOG_NAME': 'werkzeug.log'
}

# consul_configurations contains equivalent keys that will be used to extract
# configuration values from Consul.
consul_configurations = [  # (consul key, config key)
    ('flask_host', 'HOST'),
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

if environ.get('USE_ENV_VARS') == 'TRUE':  # use env variables
    for _, key in consul_configurations:
        if key in environ:
            config[key] = environ[key]
        elif key not in config:  # fail if there is not a default for the key
            raise Exception("Critical config variable {} is missing. "
                            "You probably need to run either: \n\n\tsource "
                            "config/<your settings file> \n\tor \n\t"
                            "./config/setup_consul_<environment>.sh".format(
                                key))

else:
    from consul import Consul
    kv = Consul().kv  # initalize client to KV store

    # get values from Consul and set the corresponding config variable to the
    # value retrieved from Consul.
    for consul_key, config_key in consul_configurations:
        _, consul_value = kv.get("adi-website/{}".format(consul_key))
        # fail if there is value cannot be found or it is an empty string
        if not consul_value or not consul_value.get('Value'):
            raise Exception(("No value found in Consul for key "
                             "adi-website/{}. You probably need to run: \n\n\t"
                             "./config/setup_consul_<environment>.sh")
                            .format(consul_key))
        config[config_key] = consul_value.get('Value')

# basic flask settings
config['PORT'] = int(config['PORT'])
config['DEBUG'] = (config['DEBUG'] == 'TRUE')

# Google Auth
# This is used for the webapp that allows Google+ login
config['GOOGLE_AUTH_ENABLED'] = (config['GOOGLE_AUTH_ENABLED'] == 'TRUE')

# Setup Google Auth
if config['GOOGLE_AUTH_ENABLED']:
    try:
        with open(config['CLIENT_SECRETS_PATH'], 'r') as f:
            _secrets_data = json.loads(f.read())['web']
            config['GOOGLE_CLIENT_ID'] = _secrets_data['client_id']
            if not _secrets_data.get('client_secret', None):
                raise Exception('Google Auth config file, {}, missing client '
                                'secret'.format(config['CLIENT_SECRETS_PATH']))
                exit(1)

    except IOError:
        raise Exception("The Google client_secrets file was not found at '{}',"
                        " check that it exists.".format(
                            config['CLIENT_SECRETS_PATH']))
        exit(1)

# Cross-site request forgery settings
config['CSRF_ENABLED'] = (config['CSRF_ENABLED'] == 'TRUE')

# Mongo configs
config['MONGODB_SETTINGS'] = {'DB': config['MONGO_DATABASE']}

############################################################################
#  Constants in version control
############################################################################

# Base directory
config['BASEDIR'] = path.abspath(path.join(path.dirname(__file__), pardir))

config['RELATIVE_UPLOAD_FOLDER'] = 'app/static/img/uploaded/'
config['UPLOAD_FOLDER'] = path.join(config['BASEDIR'],
                                    config['RELATIVE_UPLOAD_FOLDER'])
config['RELATIVE_DELETE_FOLDER'] = 'app/static/img/uploaded/deleted/'
config['DELETE_FOLDER'] = path.join(config['BASEDIR'],
                                    config['RELATIVE_DELETE_FOLDER'])

# The file extensions that may be uploaded
ALLOWED_UPLOAD_EXTENSIONS = set(['.png', '.jpg', '.jpeg', '.gif'])

config['DEVFEST_BANNER'] = False
