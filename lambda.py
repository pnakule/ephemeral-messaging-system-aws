import boto3
import os

def lambda_handler(event, context):

    asg_name = os.environ["ASG_NAME"]
    rds_instance_id = os.environ["RDS_INSTANCE_ID"]
    region = os.environ.get("AWS_REGION_NAME", "us-east-1")

    autoscaling = boto3.client("autoscaling", region_name=region)
    rds = boto3.client("rds", region_name=region)

    action = event.get("action")

    if action == "start":

        # Start RDS
        rds.start_db_instance(
            DBInstanceIdentifier=rds_instance_id
        )

        # Update ASG Capacity
        autoscaling.update_auto_scaling_group(
            AutoScalingGroupName=asg_name,
            MinSize=1,
            DesiredCapacity=1,
            MaxSize=3
        )

        print("Infrastructure STARTED")

    elif action == "stop":

        # Scale ASG to 0
        autoscaling.update_auto_scaling_group(
            AutoScalingGroupName=asg_name,
            MinSize=0,
            DesiredCapacity=0
        )

        # Stop RDS
        rds.stop_db_instance(
            DBInstanceIdentifier=rds_instance_id
        )

        print("Infrastructure STOPPED")

    return {
        "status": "done",
        "action": action
    }
