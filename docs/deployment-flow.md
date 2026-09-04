# Deployment Flow

This example separates credential-free pull-request validation from an explicitly dispatched AWS-authenticated Terraform plan.

## Quick Path

```bash
export ATMOS_STACKS_NAME_PATTERN='{environment}'
cd infrastructure
atmos terraform plan aws/ecs-fargate-service -s dev
atmos terraform apply aws/ecs-fargate-service -s dev
```

The repository keeps stack naming outside `atmos.yaml` so adopters can choose their own convention. The example environment variable maps the manifest at `stacks/dev/eu-west-2.yaml` to the logical stack name `dev` without changing the infrastructure configuration.

Use the commands above only after replacing placeholder values in the stack file, configuring your own AWS credentials, and reviewing the role, network, and service inputs. The included GitHub Actions workflow does not run `terraform apply`.

## What the Included Workflow Actually Runs

### Pull requests: credential-free validation

For matching pull requests, the `validate` job runs without AWS credentials. It performs:

1. Python regression tests for repository validation helpers.
2. Local Markdown link validation.
3. Terraform formatting checks.
4. Backend-free Atmos/Terraform validation of the example component.

It does **not** request an AWS OIDC token, contact a live AWS account, run `terraform plan`, publish an image, or update ECS.

### Manual dispatch: authenticated plan

When `terraform-plan.yml` is started with `workflow_dispatch`, the validation job runs first. If it succeeds, the `plan` job:

1. Requests a GitHub OIDC token.
2. Assumes the configured example AWS role using short-lived credentials.
3. Runs `atmos terraform plan` for the selected component and stack.

The included workflow stops at plan. Applying infrastructure, publishing a container image, promoting an image, and updating an ECS service are production-delivery steps that an adopter must design and approve separately.

## Adoption Order

1. Review `infrastructure/atmos.yaml` to understand component and stack locations.
2. Review `infrastructure/stacks/dev/eu-west-2.yaml` for environment-specific values.
3. Review `infrastructure/components/terraform/aws/ecs-fargate-service/` for reusable ECS logic.
4. Replace placeholder account, VPC, subnet, load balancer, target group, role, and image values.
5. Run credential-free validation before any authenticated plan.
6. Run and review a Terraform plan before applying anything.
7. Add environment protection, approval gates, image publication, and deployment automation before using the pattern for shared environments.

## Image Versioning

For real deployments, avoid using `latest` for application containers. Prefer immutable tags such as:

- Git commit SHA
- Release version
- Build number

The `container_version` variable is designed to be passed from CI/CD at deployment time.

## Promotion Model

A simple production promotion model is:

- Build once
- Push image once
- Promote the same immutable image through dev, staging, and production
- Keep environment differences in stack files, not in the container image

This promotion pipeline is a recommended extension; it is not implemented by the repository's current workflow.

## Not Production-Ready Until Reviewed

Before adopting this pattern in a real account, review:

- Role scope
- Sensitive configuration handling
- Security groups and subnet placement
- Load balancer listener and target group configuration
- Health check path and thresholds
- Logging and retention settings
- Rollback and incident response process
- Build, image-promotion, approval, and apply controls that are outside the included workflow
