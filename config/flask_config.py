from os import environ

########################
# Flask configurations #
########################

HOST = environ.get('HOST', '0.0.0.0')
PORT = int(environ.get('PORT', '5000'))
DEBUG = (environ.get('DEBUG', 'FALSE') == 'TRUE')
SECRET_KEY = environ.get('SECRET_KEY', None)
CSRF_SESSION_KEY = environ.get('CSRF_SESSION_KEY', None)

######################
# ADI configurations #
######################

DEFAULT_EVENT_IMAGE = 'img/events/default_event.png'
DEFAULT_PROFILE_PICTURE = 'img/default_profile_picture.jpg'
DEVFEST_BANNER = False

# Data paths
RESOURCES_PATH = 'data/resources.json'
LABS_DATA_PATH = 'data/labs_data.json'
COMPANIES_PATH = 'data/companies.json'

##########################
# Eventum configurations #
##########################

EVENTUM_GOOGLE_AUTH_ENABLED = (environ.get('EVENTUM_GOOGLE_AUTH_ENABLED',
                                           'TRUE') == 'TRUE')
EVENTUM_INSTALLED_APP_CLIENT_SECRET_PATH = (
    environ.get('EVENTUM_INSTALLED_APP_CLIENT_SECRET_PATH',
                'config/installed_app_client_secrets.json'))
EVENTUM_INSTALLED_APP_CREDENTIALS_PATH = (
    environ.get('EVENTUM_INSTALLED_APP_CREDENTIALS_PATH',
                'config/installed_app_credentials.json'))
EVENTUM_CLIENT_SECRETS_PATH = environ.get('EVENTUM_CLIENT_SECRETS_PATH',
                                          'config/client_secrets.json')
EVENTUM_PRIVATE_CALENDAR_ID = environ.get('EVENTUM_PRIVATE_CALENDAR_ID', None)
EVENTUM_PUBLIC_CALENDAR_ID = environ.get('EVENTUM_PUBLIC_CALENDAR_ID', None)

EVENTUM_UPLOAD_FOLDER = environ.get('EVENTUM_UPLOAD_FOLDER', 'app/static/img/uploaded/')
EVENTUM_DELETE_FOLDER = environ.get('EVENTUM_DELETE_FOLDER', 'app/static/img/uploaded/deleted/')