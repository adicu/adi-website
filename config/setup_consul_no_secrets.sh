#!/bin/sh

# flask settings
curl -X PUT -d '0.0.0.0' http://localhost:8500/v1/kv/adi-website/flask_host
curl -X PUT -d '5000' http://localhost:8500/v1/kv/adi-website/flask_port
curl -X PUT -d 'TRUE' http://localhost:8500/v1/kv/adi-website/flask_debug
curl -X PUT -d 'INSERT_YOUR_KEY' http://localhost:8500/v1/kv/adi-website/secret_key

# google related credentials
curl -X PUT -d 'client_secrets.json' http://localhost:8500/v1/kv/adi-website/installed_app_client_secret_path
curl -X PUT -d 'config/credentials.json' http://localhost:8500/v1/kv/adi-website/installed_app_credentials_path
curl -X PUT -d 'FALSE' http://localhost:8500/v1/kv/adi-website/google_auth_enabled
curl -X PUT -d 'config/client_secrets.json' http://localhost:8500/v1/kv/adi-website/client_secrets_path

# cross-site request forgery settings
curl -X PUT -d 'TRUE' http://localhost:8500/v1/kv/adi-website/csrf_enabled
curl -X PUT -d '' http://localhost:8500/v1/kv/adi-website/csrf_session_key

# calendar settings
curl -X PUT -d '' http://localhost:8500/v1/kv/adi-website/private_calendar_id
curl -X PUT -d '' http://localhost:8500/v1/kv/adi-website/public_calendar_id

# mongodb settings
curl -X PUT -d 'eventum' http://localhost:8500/v1/kv/adi-website/mongo_database

# logging settings
curl -X PUT -d '256' http://localhost:8500/v1/kv/adi-website/log_file_max_size
curl -X PUT -d 'log/app.log' http://localhost:8500/v1/kv/adi-website/app_log_name
curl -X PUT -d 'log/werkzeug.log' http://localhost:8500/v1/kv/adi-website/werkzeug_log_name