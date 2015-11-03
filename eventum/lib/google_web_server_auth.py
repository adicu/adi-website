import json
from flask import current_app


def set_web_server_client_id():
    if not current_app.config['GOOGLE_AUTH_ENABLED']:
        return

    # Setup Google Auth
    _secrets_path = current_app.config['CLIENT_SECRETS_PATH']
    try:
        with open(_secrets_path, 'r') as f:
            _secrets_data = json.loads(f.read())['web']
            current_app.config['GOOGLE_CLIENT_ID'] = _secrets_data['client_id']
            if not _secrets_data.get('client_secret', None):
                raise Exception('Google Auth config file, {}, missing '
                                'client secret'.format(_secrets_path))

    except IOError:
        raise Exception('The Google client_secrets file was not found at '
                        '{}, check that it exists.'.format(_secrets_path))
