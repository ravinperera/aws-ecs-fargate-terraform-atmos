# Deployment Flow

This example uses GitHub Actions and Terraform Atmos to plan and apply an ECS Fargate service component.

## Quick Path

```bash
cd infrastructure
atmos terraform plan aws/ecs-fargate-service -s dev/eu-west-2
atmos terraform apply aws/ecs-fargate-service -s dev/eu-west-2
```

Use the commands above only after replacing placeholder values in the stack file and reviewing the role, network, and service inputs.

## Flow

1. A developer opens a pull request or pushes to the default branch.
2. The workflow obtains temporary cloud credentials.
3. The workflow runs Terraform format, validation, and plan.
4. A reviewed apply workflow can deploy the selected Atmos component.

## Adoption Order

1. Review `infrastructure/atmos.yaml` to understand component and stack locations.
2. Review `infrastructure/stacks/dev/eu-west-2.yaml` for environment-specific values.
3. Review `infrastructure/components/terraform/aws/ecs-fargate-service/` for reusable ECS logic.
4. Replace placeholder account, VPC, subnet, load balancer, target group, role, and image values.
5. Run a plan before applying anything.
6. Add environment protection and approval gates before using the pattern for shared environments.

## Image Versioning

For real deployments, avoid using `latest` for application containers. Prefer immutable tags such as:

- Git commit SHA
- Release version
- Build number

The `container_version` variable is designed to be passed from CI/CD at deployment time.

## Promotion Model

A simple promotion model is:

- Build once
- Push image once
- Promote the same image tag through dev, staging, and production
- Keep environment differences in stack files, not in the container image

## Not Production-Ready Until Reviewed

Before adopting this pattern in a real account, review:

- Role scope
- Sensitive configuration handling
- Security groups and subnet placement
- Load balancer listener and target group configuration
- Health check path and thresholds
- Logging and retention settings
- Rollback and incident response process
