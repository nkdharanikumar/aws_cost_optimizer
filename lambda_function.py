import boto3

ec2 = boto3.client('ec2')
sns = boto3.client('sns')

TOPIC_ARN = "arn:aws:sns:ap-south-1:432180555230:cost-optimizer-report"

SNAPSHOT_COST_PER_GB = 0.05
VOLUME_COST_PER_GB = 0.08
T3_MICRO_MONTHLY = 8


def delete_snapshots():

    deleted_snapshots = []
    cost_saved = 0

    snapshots = ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']

    for snapshot in snapshots:

        snapshot_id = snapshot['SnapshotId']
        size = snapshot['VolumeSize']

        ec2.delete_snapshot(SnapshotId=snapshot_id)

        snapshot_cost = size * SNAPSHOT_COST_PER_GB
        cost_saved += snapshot_cost

        print(f"{snapshot_id} deleted (snapshot cleanup)")

        deleted_snapshots.append(snapshot_id)

    return deleted_snapshots, cost_saved


def delete_unattached_volumes():

    deleted_volumes = []
    cost_saved = 0

    volumes = ec2.describe_volumes()['Volumes']

    for volume in volumes:

        volume_id = volume['VolumeId']
        state = volume['State']
        size = volume['Size']

        print(f"Volume {volume_id} state: {state}")

        if state == "available":

            ec2.delete_volume(VolumeId=volume_id)

            volume_cost = size * VOLUME_COST_PER_GB
            cost_saved += volume_cost

            print(f"{volume_id} deleted because it is unattached")

            deleted_volumes.append(volume_id)

    return deleted_volumes, cost_saved


def delete_stopped_instances():

    deleted_instances = []
    cost_saved = 0

    reservations = ec2.describe_instances()['Reservations']

    for res in reservations:

        for inst in res['Instances']:

            instance_id = inst['InstanceId']
            state = inst['State']['Name']
            instance_type = inst['InstanceType']

            print(f"Instance {instance_id} state: {state}")

            if state == "stopped":

                ec2.terminate_instances(InstanceIds=[instance_id])

                if instance_type == "t3.micro":
                    cost_saved += T3_MICRO_MONTHLY

                print(f"{instance_id} terminated because it was stopped")

                deleted_instances.append(instance_id)

    return deleted_instances, cost_saved


def send_report(snapshots, volumes, instances, snap_cost, vol_cost, inst_cost):

    total = snap_cost + vol_cost + inst_cost

    report = f"""
AWS COST OPTIMIZATION REPORT

Snapshots Deleted:
{snapshots}

Volumes Deleted:
{volumes}

Instances Terminated:
{instances}

Estimated Monthly Cost Saved:

Snapshots: ${round(snap_cost,2)}
Volumes: ${round(vol_cost,2)}
Instances: ${round(inst_cost,2)}

Total Estimated Savings: ${round(total,2)}
"""

    sns.publish(
        TopicArn=TOPIC_ARN,
        Message=report,
        Subject="AWS Cost Optimization Report"
    )

    print("Report sent successfully")


def lambda_handler(event, context):

    print("Starting AWS cost optimization scan...")

    snapshots, snap_cost = delete_snapshots()
    volumes, vol_cost = delete_unattached_volumes()
    instances, inst_cost = delete_stopped_instances()

    send_report(snapshots, volumes, instances, snap_cost, vol_cost, inst_cost)

    print("Execution completed")