# AWS Serverless Cost Optimization System

A serverless automation system that detects and removes unused AWS
resources to reduce cloud costs.

This project automatically: - Deletes **EBS Snapshots** - Deletes
**Unattached EBS Volumes** - Terminates **Stopped EC2 Instances** -
Sends an **Automated Email Report** - Estimates **Monthly Cost Savings**

------------------------------------------------------------------------

## Architecture

EventBridge Scheduler → AWS Lambda → EC2/EBS Cleanup → SNS Email
Notification → CloudWatch Logs

AWS Services Used: - AWS Lambda - Amazon EventBridge - Amazon EC2 -
Amazon Elastic Block Store (EBS) - Amazon Simple Notification Service
(SNS) - Amazon CloudWatch

------------------------------------------------------------------------

## Features

-   Automated cloud infrastructure cleanup
-   Serverless architecture
-   Email reporting using SNS
-   Scheduled automation using EventBridge
-   Logging and monitoring with CloudWatch
-   Estimated cost savings calculation

------------------------------------------------------------------------

## How It Works

1.  **Amazon EventBridge** triggers the Lambda function on a schedule.
2.  The **AWS Lambda** function runs Python code using **boto3**.
3.  The script scans AWS resources and identifies:
    -   EBS Snapshots
    -   Unattached EBS Volumes
    -   Stopped EC2 Instances
4.  The system deletes unused resources automatically.
5.  A **cost optimization report** is sent via SNS email.
6.  Execution logs are stored in **CloudWatch**.

------------------------------------------------------------------------

## Example Email Report

AWS COST OPTIMIZATION REPORT

Snapshots Deleted: \['snap-xxxx'\]

Volumes Deleted: \['vol-xxxx'\]

Instances Terminated: \['i-xxxx'\]

Estimated Monthly Cost Saved:

Snapshots: \$X Volumes: \$Y Instances: \$Z

Total Estimated Savings: \$N

------------------------------------------------------------------------

## Project Demonstration

Screenshots included in this repository:

1.  Lambda Function Code
2.  EventBridge Scheduler Configuration
3.  Lambda Execution Logs
4.  SNS Email Report

These screenshots demonstrate the full automation pipeline.

------------------------------------------------------------------------

## Technologies Used

Python\
boto3 (AWS SDK for Python)\
AWS Lambda\
Amazon EC2\
Amazon EBS\
Amazon SNS\
Amazon EventBridge\
Amazon CloudWatch

------------------------------------------------------------------------

## Project Motivation

Cloud environments often accumulate unused resources such as snapshots,
idle volumes, and stopped instances.\
These resources increase infrastructure costs over time.

This project demonstrates how **serverless automation** can be used to:

-   Identify unused cloud resources
-   Automatically clean infrastructure
-   Reduce AWS costs
-   Implement DevOps automation practices

------------------------------------------------------------------------

## Author

DK
DevOps / Cloud Enthusiast
