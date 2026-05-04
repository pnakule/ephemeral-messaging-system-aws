# Ephemeral Messaging System on AWS

## Overview (note:Updates are being made to the ephemeral messaging system.)

This project is a simple web application that allows users to create messages that can be viewed once and then expire. The system is designed using AWS services with a focus on secure architecture, controlled access, and basic automation.

---

## Architecture Summary

The application follows a layered architecture:

1. User accesses the application using a domain (`www.elevateaws.com`)
2. DNS is managed using Route 53
3. Traffic is routed through CloudFront
4. CloudFront forwards requests to an Application Load Balancer (ALB)
5. ALB routes traffic via a Target Group to an EC2 instance
6. The EC2 instance runs a Flask application (served using Gunicorn)
7. The application interacts with an RDS (MySQL) database
8. If the backend is unavailable, CloudFront serves a static offline page from S3

---

## Key AWS Services Used

* **Route 53** – Domain routing to CloudFront
* **CloudFront** – Edge routing and failover (ALB → S3)
* **Application Load Balancer** – Request routing and health checks
* **EC2** – Hosts the Flask application
* **RDS (MySQL)** – Stores application data
* **S3** – Static offline page (failover)
* **Lambda** – Controls start/stop of EC2 and RDS
* **EventBridge** – Schedules automation
* **Systems Manager (Session Manager)** – Secure EC2 access
* **Parameter Store** – Stores database credentials
* **KMS** – Encryption for secrets and storage
* **IAM** – Role-based access control

---

## Networking Design

* VPC with two Availability Zones
* Public subnet:

  * ALB
  * NAT Gateway
* Private subnet:

  * EC2
  * RDS

### Traffic Flow

* **Inbound:**
  User → CloudFront → ALB → EC2

* **Database Access:**
  EC2 → RDS (private connection)

* **Outbound (updates, installs):**
  EC2 → NAT Gateway → Internet Gateway → Internet

---

## Security Design

* No direct public access to EC2 and RDS
* Access controlled using Security Groups:

  * ALB → EC2 (port 5000)
  * EC2 → RDS (port 3306)
* EC2 access via Session Manager (no SSH keys)
* Secrets stored in Parameter Store (no hardcoding)
* Encryption enabled using KMS

---

## Failover Handling

CloudFront is configured with:

* Primary origin → ALB
* Failover origin → S3

If the application becomes unhealthy, users are redirected to a static offline page.

---

## Automation (Cost Optimization)

To reduce cost, resources are scheduled:

* EventBridge triggers Lambda functions
* Lambda performs:

  * Start EC2 and RDS
  * Stop EC2 and RDS

### Schedule

* Start: 7 PM IST
* Stop: 8 PM IST

---

## Application Details

* Backend: Flask
* Server: Gunicorn
* Database: MySQL (RDS)

### Features

* One-time message viewing
* Auto-delete after viewing
* Expiry-based message removal

---

## Challenges Faced

### 1. EventBridge not triggering Lambda

* Issue: Rule created but Lambda not executing
* Fix: Added correct resource-based permission for EventBridge

---

### 2. Time mismatch in scheduling

* Issue: Incorrect execution time
* Fix: Adjusted cron expression using UTC

---

### 3. CloudFront failover not working

* Issue: Offline page not served
* Fix: Configured origin failover with proper 5xx error codes

---

## Current Limitations

* Single EC2 instance (no autoscaling)
* Single-region deployment
* Basic monitoring (no advanced alerts)

---

## Future Improvements

* Add Auto Scaling Group
* Add CloudWatch alarms and monitoring
* Restrict ALB access to CloudFront only
* Improve CI/CD pipeline

---

## Conclusion

This project demonstrates a practical AWS architecture with:

* Controlled access using security groups
* Private networking for backend services
* Event-driven automation
* Failover handling using CloudFront

The focus was on understanding how services connect and behave in a real setup rather than building a complex system.

---


