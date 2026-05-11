import boto3

# Database configuration
# values are securely fetched from AWS Systems Manager Parameter Store.
# This avoids hardcoding credentials and improves security.

ssm = boto3.client("ssm", region_name="us-east-1")

def get_param(name, decrypt=False):
    return ssm.get_parameter(
        Name=name,
        WithDecryption=decrypt
    )["Parameter"]["Value"]

DB_CONFIG = {
    "host": get_param("/ephemeral/db/host"),
    "user": get_param("/ephemeral/db/user"),
    "password": get_param("/ephemeral/db/password", decrypt=True),
    "database": get_param("/ephemeral/db/name"),
    "port": 3306,
}
