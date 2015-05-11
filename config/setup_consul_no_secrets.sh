#!/bin/sh

consul_set() {
	curl -X PUT -d '$2' 'http://localhost:8500/v1/kv/adi-website/$1'
}

# flask settings
consul_set flask_host '0.0.0.0'
consul_set flask_port '5000'
consul_set flask_debug 'TRUE'
consul_set secret_key ''

# google related credentials
consul_set installed_app_client_secret_path 'config/installed_app_client_secrets.json'
consul_set installed_app_credentials_path 'config/installed_app_credentials.json'
consul_set google_auth_enabled 'FALSE'
consul_set client_secrets_path 'config/client_secrets.json'

# cross-site request forgery settings
consul_set csrf_enabled 'TRUE'
consul_set csrf_session_key ''

# calendar settings
consul_set private_calendar_id ''
consul_set public_calendar_id ''

# mongodb settings
consul_set mongo_database 'eventum'

# logging settings
consul_set log_file_max_size '256'
consul_set app_log_name 'log/app.log'
consul_set werkzeug_log_name 'log/werkzeug.log'