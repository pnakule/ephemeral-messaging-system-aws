# EphemeralDrop – AWS-Based Ephemeral Messaging System

## Overview

EphemeralDrop is a simple web application where users can create a secret message and share it through a link.
The message can be viewed only once or expires after 24 hours.

This project focuses on running infrastructure only when needed to reduce cost.

---

## 🎯 Objective

* Reduce cloud cost by stopping resources when not in use
* Automate infrastructure using scheduled events
* Build a secure setup without exposing backend services

---

## Architecture (Flow)

```text
User → Route 53 → CloudFront → ALB → EC2 → RDS
```

### Request Flow

1. User accesses www.elevateaws.com
2. Domain is resolved using Route 53
3. Request goes to CloudFront
4. CloudFront forwards traffic to ALB
5. ALB forwards request to Target Group
6. Target Group routes traffic to EC2 (Flask app)
7. Application reads/writes data to RDS

---

##  Failover (Fallback)

* If EC2 becomes unhealthy
* CloudFront switches to a secondary origin
* Secondary origin = S3 bucket (static website [Shows a simple offline page)]

---

## Infrastructure Setup

### Network

* 1 VPC with 2 Availability Zones

**AZ-1**

* Public subnet (ALB)
* Private subnet (EC2 + RDS)

**AZ-2**

* Private subnet (reserved for high availability and future scaling)

---

### Compute & Database

* EC2 runs Flask application
* RDS stores messages

Both are in **private subnet (no public access)**

---

### Load Balancing

* ALB handles incoming traffic
* Uses Target Group to route traffic to EC2

---

## 🔐 Security

* EC2 instances are in private subnets (no public access)
* Access to EC2 is done using Session Manager (no SSH keys required)
* Database credentials are stored securely in SSM Parameter Store
* Sensitive data is encrypted using KMS

---

## Automation

Used:

* EventBridge
* Lambda

### Flow

```text
EventBridge → Lambda → Start/Stop EC2 + RDS
```

* Two rules:

  * Start resources
  * Stop resources

* Used UTC-based cron scheduling since EventBridge runs on UTC  
* Added buffer time to account for RDS startup delay  

---

## Application Logic

* A simple Flask-based app is used to create and view messages
* Each message is stored with a unique ID and accessed through a link

Features:

* Message can be viewed only once
* It is deleted after being viewed
* If not opened, it expires after 24 hours

---

## 🧩 AWS Services Used

* CloudFront
* Route 53
* ALB
* EC2
* RDS
* S3
* EventBridge
* Lambda
* IAM
* Systems Manager
* KMS

---

## Challenges & Fixes

### 1. CloudFront failover was not working initially
Took some time to understand how origin failover works and how CloudFront decides when to switch to S3.
### 2. EventBridge and Lambda connection was confusing at first
I assumed a role was enough, but later understood Lambda needs a separate permission for EventBridge.
### 3. Delay in startup
* Issue: App not ready on exact time
* Fix: Added buffer time

---

## Summary

> Built a cost-aware AWS architecture where EC2 and RDS are automatically started and stopped using EventBridge and Lambda, while keeping the system secure and simple.

---

## Future Improvements

* Auto Scaling (separate setup)
* monitoring (CloudWatch alarms)

