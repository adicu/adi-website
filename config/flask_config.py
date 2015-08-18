from os import path, pardir
import json
import requests

# The Flask app configures itself from this dictionary
# Values are initialized to default values, or `None`.
config = {

    # Flask configurations
    'HOST': 'localhost',
    'PORT': 5000,
    'DEBUG': False,
    'SECRET_KEY': None,

    # Cross-site request forgery configurations
    'CSRF_SESSION_KEY': None,
    'CSRF_ENABLED': True,

    # Google+, Google Auth, and Google Calendar configurations
    'GOOGLE_AUTH_ENABLED': True,
    'INSTALLED_APP_CLIENT_SECRET_PATH':
        'config/installed_app_client_secrets.json',
    'INSTALLED_APP_CREDENTIALS_PATH': 'config/installed_app_credentials.json',
    'CLIENT_SECRETS_PATH': 'config/client_secrets.json',
    'PRIVATE_CALENDAR_ID': None,
    'PUBLIC_CALENDAR_ID': None,

    # MongoDB configurations
    'MONGO_DATABASE': 'eventum',

    # Logging configurations
    'LOG_FILE_MAX_SIZE': '256',
    'APP_LOG_NAME': 'app.log',
    'WERKZEUG_LOG_NAME': 'werkzeug.log',
}

from consul import Consul
kv = Consul().kv  # initalize client to KV store

# get values from Consul and set the corresponding config variable to the
# value retrieved from Consul.
for key, value in config.iteritems():
    try:
        _, consul_value = kv.get(("adi-website/{}").format(key))
    except requests.ConnectionError:
        raise Exception('Failed to connect to Consul.  You probably need to '
                        'run: \n\n\t./config/run_consul.sh')

    # We have a good value in Consul
    if consul_value and consul_value.get('Value'):
        config[key] = consul_value.get('Value')
        continue

    # We can use the default value if it's not None
    if value is not None:
        continue

    # Fail if there is value cannot be found or it is an empty string
    raise Exception(("No default value found in Consul for key "
                     "adi-website/{}. You probably need to run: \n\n\t"
                     "./config/setup_consul_<environment>.sh")
                    .format(key))

# Cast strings to appropiate types: int, bool, dictionary
config['PORT'] = int(config['PORT'])
config['DEBUG'] = (config['DEBUG'] == 'TRUE')
config['GOOGLE_AUTH_ENABLED'] = (config['GOOGLE_AUTH_ENABLED'] == 'TRUE')
config['CSRF_ENABLED'] = (config['CSRF_ENABLED'] == 'TRUE')
config['MONGODB_SETTINGS'] = {'DB': config['MONGO_DATABASE']}

# Setup Google Auth
if config['GOOGLE_AUTH_ENABLED']:
    try:
        with open(config['CLIENT_SECRETS_PATH'], 'r') as f:
            _secrets_data = json.loads(f.read())['web']
            config['GOOGLE_CLIENT_ID'] = _secrets_data['client_id']
            if not _secrets_data.get('client_secret', None):
                raise Exception('Google Auth config file, {}, missing client '
                                'secret'.format(config['CLIENT_SECRETS_PATH']))

    except IOError:
        raise Exception("The Google client_secrets file was not found at '{}',"
                        " check that it exists.".format(
                            config['CLIENT_SECRETS_PATH']))

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
config['ALLOWED_UPLOAD_EXTENSIONS'] = set(['.png', '.jpg', '.jpeg', '.gif'])

config['DEFAULT_PROFILE_PICTURE'] = 'img/default_profile_picture.jpg'

config['DEVFEST_BANNER'] = False
