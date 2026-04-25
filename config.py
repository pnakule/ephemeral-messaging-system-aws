import os

# ---------------------------------------------------------------------------
# Database configuration
# On AWS EC2, set these as environment variables instead of hardcoding.
# Example:
#   export DB_HOST="your-rds-endpoint.rds.amazonaws.com"
#   export DB_USER="admin"
#   export DB_PASSWORD="yourpassword"
#   export DB_NAME="ephemeral_db"
# ---------------------------------------------------------------------------

DB_CONFIG = {
    "host": "localhost",
    "user": "appuser",
    "password": "app123",
    "database": "ephemeral_db",
    "port": 3306,
}
