# Ephemeral Messaging System on AWS

## Overview

### Project Goals


- Understand how a real web application is deployed and works on AWS from start to end  
- Learn how scaling, security, HTTPS, failover, and automation work in cloud systems  
- Understand how different AWS services connect and work together  
- Learn AWS pricing and ways to reduce running cost 

This is a simple secure one-time messaging web application built on AWS.

Users can create secret messages, share links, and messages disappear after one view or expiration timeout.

> Important  
> To reduce AWS cost, this infrastructure runs only for 1 hour daily using EventBridge + Lambda automation.  
> Because of this, generated links may not work outside the scheduled runtime window.

---

## Architecture Diagram

![Architecture Diagram](ephemeral-architecture.png)

---

## AWS Services Used

| Service | Used for |
|---|---|
| Route 53 | DNS routing |
| CloudFront | HTTPS delivery and failover,  Custom Security Header |
| ACM | SSL certificate |
| ALB | Traffic distribution to Healty Instances|
| Auto Scaling Group | EC2 scaling and self-healing |
| EC2 | Flask application hosting |
| RDS MySQL | Database |
| S3 | Offline/failover Static page |
| IAM | Secure service permissions and access control |
| Systems Manager | Secure EC2 access |
| Parameter Store | Store secrets and DB configs |
| Lambda | Infrastructure automation |
| EventBridge | Scheduled start/stop |

---

## Cost Breakdown

## Future Improvemts
- Add CI/CD pipeline to automatically deploy application updates from GitHub
- Add CloudWatch monitoring and alerts for infrastructure health and application logs
- Upgrade RDS to Multi-AZ deployment for higher availability
- Add AWS WAF for additional web application security



