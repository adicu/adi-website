#!/bin/sh

# flask settings
curl -X PUT -d 'localhost' http://localhost:8500/v1/kv/adi-website/flask_host
curl -X PUT -d '5000' http://localhost:8500/v1/kv/adi-website/flask_port
curl -X PUT -d 'TRUE' http://localhost:8500/v1/kv/adi-website/flask_debug
curl -X PUT -d '\xcb\x87Puf\xf5P\xfc;\x8a\x1bO\xd6\xd0\t\xa7\xdd\x1a\x0b}\xa5\r\xd4z' http://localhost:8500/v1/kv/adi-website/secret_key

# google related credentials
curl -X PUT -d 'client_secrets.json' http://localhost:8500/v1/kv/adi-website/installed_app_client_secret_path
curl -X PUT -d 'config/credentials.json' http://localhost:8500/v1/kv/adi-website/installed_app_credentials_path
curl -X PUT -d 'FALSE' http://localhost:8500/v1/kv/adi-website/google_auth_enabled
curl -X PUT -d 'config/client_secrets.json' http://localhost:8500/v1/kv/adi-website/client_secrets_path

# cross-site request forgery settings
curl -X PUT -d 'TRUE' http://localhost:8500/v1/kv/adi-website/csrf_enabled
curl -X PUT -d ']\x84\xa0\xe4PB\x9a\x94[\x0bA\x8bs\x17\x04\x07\xd2\xd2\xbf\x80\xdf\xae\xd1\x89' http://localhost:8500/v1/kv/adi-website/csrf_session_key

# calendar settings
curl -X PUT -d 'puobtm1j1aq2lme38gj1sokdoc@group.calendar.google.com' http://localhost:8500/v1/kv/adi-website/private_calendar_id
curl -X PUT -d 'v6hbf5ninkutr5qeutjgohpaj8@group.calendar.google.com' http://localhost:8500/v1/kv/adi-website/public_calendar_id

# mongodb settings
curl -X PUT -d 'eventum' http://localhost:8500/v1/kv/adi-website/mongo_database

# logging settings
curl -X PUT -d '256' http://localhost:8500/v1/kv/adi-website/log_file_max_size
curl -X PUT -d 'log/app.log' http://localhost:8500/v1/kv/adi-website/app_log_name
curl -X PUT -d 'log/werkzeug.log' http://localhost:8500/v1/kv/adi-website/werkzeug_log_name

