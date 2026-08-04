# AWS ECS Fargate Terraform Atmos Pattern

Production-style AWS ECS Fargate deployment pattern using Terraform, Atmos, GitHub Actions, and AWS OIDC.

This repository is a public reference implementation for deploying containerized workloads to AWS ECS Fargate using a reusable infrastructure-as-code structure. It is intentionally generic and does not include company-specific configuration, secrets, account IDs, or client data.

## 30-Second Quick Start

Use this repo as a reference pattern for structuring an ECS/Fargate service with Terraform and Atmos.

Before running the example, install Terraform and Atmos, then review the placeholder values for the target AWS account. Planning and applying require AWS credentials with permissions appropriate to the resources being evaluated; this repository does not provide credentials.

The quick-start commands use these files:

```text
infrastructure/
├── atmos.yaml
├── stacks/dev/eu-west-2.yaml
└── components/terraform/aws/ecs-fargate-service/
    ├── main.tf
    ├── variables.tf
    └── outputs.tf
```

```bash
# 1. Review the Atmos stack inputs
cat infrastructure/stacks/dev/eu-west-2.yaml

# 2. Review the reusable ECS component
ls infrastructure/components/terraform/aws/ecs-fargate-service

# 3. Run a Terraform plan through Atmos
cd infrastructure
atmos terraform plan aws/ecs-fargate-service -s eu-west-2

# 4. Apply only after replacing placeholders and reviewing permissions
atmos terraform apply aws/ecs-fargate-service -s eu-west-2
```

The manifest is stored at `stacks/dev/eu-west-2.yaml`, while its Atmos stack name is `eu-west-2` because this reference project uses the stack filename as the default logical name.

Expected adoption path:

1. Replace placeholder account, VPC, subnet, ALB, target group, IAM, and image values.
2. Keep environment-specific values in Atmos stack files.
3. Keep reusable infrastructure logic inside Terraform components.
4. Pass image versions from CI/CD rather than hardcoding `latest`.
5. Complete the [production readiness checklist](docs/deployment-readiness.md), including IAM, networking, secrets, observability, health checks, autoscaling, evidence, and rollback ownership.

See the [deployment flow](docs/deployment-flow.md) for the full adoption order, image-promotion guidance, and review points.

This is a reference pattern, not a production-ready drop-in module. Treat it as a structure to adapt and review.

## What This Demonstrates

- Multi-environment infrastructure layout using Atmos stacks
- Reusable Terraform component structure for ECS Fargate services
- GitHub Actions workflow pattern using AWS OIDC instead of long-lived access keys
- Separation of task definition, service configuration, networking, IAM, and environment inputs
- Production-oriented conventions for logs, health checks, secrets, and deployment safety

## Architecture

GitHub Actions uses AWS OIDC to assume a scoped deployment role, publish container images to ECR, and update an ECS service running in private subnets behind an Application Load Balancer. Runtime secrets come from Secrets Manager and application logs are sent to CloudWatch Logs.

See the [Mermaid architecture diagram and component notes](docs/architecture.md).

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
│   ├── deployment-flow.md
│   ├── deployment-readiness.md
│   ├── incident-and-rollback-runbook.md
│   ├── scaling-and-cost-guardrails.md
│   └── terraform-state-safety.md
├── scripts/
│   └── check_markdown_links.py
├── tests/
│   └── test_check_markdown_links.py
├── CONTRIBUTING.md
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
- [Production readiness checklist](docs/deployment-readiness.md)
- [ECS deployment incident and rollback runbook](docs/incident-and-rollback-runbook.md)
- [ECS scaling and cost guardrails](docs/scaling-and-cost-guardrails.md)
- [Terraform state safety](docs/terraform-state-safety.md)
- [Architecture](docs/architecture.md)
- [Contributing](CONTRIBUTING.md)

## Local Validation

The pull-request validation job is credential-free. It checks repository documentation, Atmos stack structure, and Terraform configuration without contacting AWS or running a plan.

Run the same checks locally:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/check_markdown_links.py .
terraform -chdir=infrastructure/components/terraform/aws/ecs-fargate-service fmt -check -recursive
cd infrastructure
atmos validate stacks
terraform -chdir=components/terraform/aws/ecs-fargate-service init -backend=false -input=false
terraform -chdir=components/terraform/aws/ecs-fargate-service validate
```

The Markdown validator checks local file targets only and deliberately skips external URLs because reliable external-link checking requires network access. The authenticated Terraform plan remains manual through `workflow_dispatch`; it requires a real OIDC role and replacement of the example account and infrastructure values.

## Status

This is a showcase/reference repository. It is designed to demonstrate architecture and implementation approach rather than deploy a real production system without adaptation.
