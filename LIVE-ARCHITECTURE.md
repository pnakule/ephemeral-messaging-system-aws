# Current Deployment Architecture Note

The original architecture for this project was designed mainly for learning AWS services integration, end-to-end deployment flow, automation, and security practices. After deploying the project and calculating the actual AWS monthly cost (shown in the cost breakdown section), I redesigned the live deployment into a more cost-optimized architecture so the project could remain publicly accessible as a live demo. While this simplified deployment does not fully follow production-level best practices, it still maintains the core AWS integrations and operational workflows at a much lower cost.

The goal of this deployment was to:
- reduce unnecessary AWS costs
- keep the application live for demonstration
- practice real-world AWS deployment workflows
- automate infrastructure operations
- integrate multiple AWS services together

This setup is mainly intended for learning and demonstration purposes.

---

## Current Live Deployment Overview

Route53 → CloudFront → EC2 (NGINX + Gunicorn + Flask + MySQL)

Fallback Flow:
CloudFront Custom Error Response → S3 Offline Page

Automation:
EventBridge → Lambda → EC2 Start/Stop + Route53 Dynamic DNS Update

Security:
IAM + SSM Session Manager + Parameter Store + OAC


# Current Live Detailed Deployment Flow

## 1. User Access

Users access the application using:

```text
www.elevateaws.com
```

Amazon Route 53 routes the request to Amazon CloudFront.

---

## 2. CloudFront HTTPS Delivery

CloudFront acts as the public entry point for the application.

It provides:
- HTTPS support using ACM certificate
- edge delivery
- caching
- custom error handling

CloudFront uses:

```text
origin.elevateaws.com
```

as the application origin.

---

## 3. Dynamic DNS Handling (Without Elastic IP)

To reduce costs and simplify the setup, Elastic IP was not used.

Instead:
- EC2 receives a new public IP whenever it starts
- AWS Lambda automatically detects the new public IP
- Lambda updates the Route 53 DNS record:

```text
origin.elevateaws.com
```

This allows CloudFront to continue reaching the EC2 instance even after IP changes.

---

## 4. EC2 Application Stack

A single EC2 instance runs:
- NGINX
- Gunicorn
- Flask application
- MySQL database

---

## 5. Secure Secret Management

Database credentials are stored securely inside:

```text
AWS Systems Manager Parameter Store
```

Secrets are encrypted using AWS KMS.

The Flask application retrieves secrets dynamically during runtime instead of hardcoding credentials.

---

## 6. Secure EC2 Access

EC2 access is managed using:

```text
AWS Systems Manager Session Manager
```

instead of public SSH access.

This avoids exposing SSH ports and SSH keys publicly.

---

## 7. Automated Start / Stop Scheduling

To reduce compute costs:
- Amazon EventBridge schedules EC2 start and stop operations
- AWS Lambda performs the automation

Lambda responsibilities:
- start EC2
- stop EC2
- update Route 53 dynamic DNS record

This keeps the demo infrastructure cost-efficient while still allowing the application to remain publicly accessible during active hours.

---

## 8. Offline Maintenance Fallback

CloudFront custom error responses are configured for:
- 502
- 503
- 504

If the EC2 application becomes unavailable:
- CloudFront automatically serves an offline maintenance page
- the offline page is stored in a private Amazon S3 bucket
- S3 access is secured using Origin Access Control (OAC)

  ## Estimated Monthly Cost (Current Live Deployment)

| Service | Approximate Monthly Cost |
|---|---|
| Route 53 Hosted Zone | ~$0.50 |
| EC2 (Linux t3.micro) + EBS | ~$1–2 |

~$2–3/month for low-traffic live demo usage.
