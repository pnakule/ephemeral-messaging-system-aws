import boto3

# Database configuration
# In production (EC2), values are securely fetched from AWS Systems Manager Parameter Store.
# This avoids hardcoding credentials and improves security.

ssm = boto3.client("ssm", region_name="us-east-1")

def get_param(name, decrypt=False):
    return ssm.get_parameter(
        Name=name,
        WithDecryption=decrypt
    )["Parameter"]["Value"]

DB_CONFIG = {
    "host": get_param("/myapp/db_host"),
    "user": get_param("/myapp/db_user"),
    "password": get_param("/myapp/db_password", decrypt=True),
    "database": get_param("/myapp/db_name"),
    "port": 3306,
}
