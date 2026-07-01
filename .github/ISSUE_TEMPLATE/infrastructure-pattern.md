---
name: Infrastructure pattern improvement
description: Propose a Terraform, Atmos, ECS, CI/CD, or AWS reference-pattern change
title: "infra: "
labels: ["enhancement"]
---

## Context

What part of the reference pattern should change?

## Proposed change

Describe the intended Terraform, Atmos, ECS, CI/CD, or AWS example update.

## Review notes

Call out any areas that need careful review, such as:

- IAM permissions
- network exposure
- secrets handling
- logging or monitoring
- deployment and rollback behaviour

## Validation

List any checks that were run or should be run.

Examples:

```bash
terraform fmt -recursive
atmos terraform validate aws/ecs-fargate-service -s dev/eu-west-2
atmos terraform plan aws/ecs-fargate-service -s dev/eu-west-2
```

## Notes

Add links, assumptions, or follow-up work.
