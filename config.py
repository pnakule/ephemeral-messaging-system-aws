import os

# On AWS EC2 set these as environment variables.
# Locally you can change the defaults below for testing.

DB_CONFIG = {
    "host":     os.environ.get("DB_HOST",     "localhost"),
    "user":     os.environ.get("DB_USER",     "appuser"),
    "password": os.environ.get("DB_PASSWORD", ""),
    "database": os.environ.get("DB_NAME",     "ephemeral_db"),
    "port":     int(os.environ.get("DB_PORT", 3306)),
}
