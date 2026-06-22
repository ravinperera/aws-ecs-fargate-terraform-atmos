# AWS ECS Fargate Terraform Atmos Pattern

Production-style AWS ECS Fargate deployment pattern using Terraform, Atmos, GitHub Actions, and AWS OIDC.

This repository is a public reference implementation for deploying containerized workloads to AWS ECS Fargate using a reusable infrastructure-as-code structure. It is intentionally generic and does not include company-specific configuration, secrets, account IDs, or client data.

## 30-Second Quick Start

Use this repo as a reference pattern for structuring an ECS/Fargate service with Terraform and Atmos.

```bash
# 1. Review the Atmos stack inputs
cat infrastructure/stacks/dev/eu-west-2.yaml

# 2. Review the reusable ECS component
ls infrastructure/components/terraform/aws/ecs-fargate-service

# 3. Run a Terraform plan through Atmos
cd infrastructure
atmos terraform plan aws/ecs-fargate-service -s dev/eu-west-2

# 4. Apply only after replacing placeholders and reviewing permissions
atmos terraform apply aws/ecs-fargate-service -s dev/eu-west-2
```

Expected adoption path:

1. Replace placeholder account, VPC, subnet, ALB, target group, IAM, and image values.
2. Keep environment-specific values in Atmos stack files.
3. Keep reusable infrastructure logic inside Terraform components.
4. Pass image versions from CI/CD rather than hardcoding `latest`.
5. Review IAM, networking, secrets, observability, and rollback behaviour before using this in a real environment.

This is a reference pattern, not a production-ready drop-in module. Treat it as a structure to adapt and review.

## What This Demonstrates

- Multi-environment infrastructure layout using Atmos stacks
- Reusable Terraform component structure for ECS Fargate services
- GitHub Actions workflow pattern using AWS OIDC instead of long-lived access keys
- Separation of task definition, service configuration, networking, IAM, and environment inputs
- Production-oriented conventions for logs, health checks, secrets, and deployment safety

## Architecture

```text
GitHub Actions
   |
   | OIDC assume role
   v
AWS Account
   |
   +-- ECR image repository
   +-- ECS Cluster
   +-- ECS Task Definition
   +-- ECS Service on Fargate
   +-- Application Load Balancer
   +-- CloudWatch Log Group
   +-- Secrets Manager
   +-- VPC private subnets
```

## Repository Structure

```text
.
├── .github/workflows/
│   └── terraform-plan.yml
├── infrastructure/
│   ├── atmos.yaml
│   ├── components/terraform/aws/ecs-fargate-service/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── stacks/dev/eu-west-2.yaml
├── docs/
│   ├── architecture.md
│   └── deployment-flow.md
└── README.md
```

## Design Principles

- Prefer short-lived AWS credentials through GitHub OIDC
- Keep Terraform components reusable and environment-neutral
- Keep environment-specific values in Atmos stack files
- Run workloads in private subnets wherever possible
- Inject sensitive values through AWS Secrets Manager, not plain environment variables
- Make CI/CD explicit, reviewable, and repeatable

## Example Use Case

This pattern fits a Django, FastAPI, Node.js, or API service deployed to ECS Fargate behind an ALB, with logs in CloudWatch and secrets managed through AWS Secrets Manager.

## Documentation

- [Deployment flow](docs/deployment-flow.md)
- [Architecture](docs/architecture.md)

## Status

This is a showcase/reference repository. It is designed to demonstrate architecture and implementation approach rather than deploy a real production system without adaptation.
