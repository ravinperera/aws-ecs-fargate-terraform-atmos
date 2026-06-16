# Deployment Flow

This example uses GitHub Actions with AWS OIDC.

## Flow

1. A developer opens a pull request or pushes to the default branch.
2. GitHub Actions requests an OIDC token from GitHub.
3. AWS validates the token against the IAM role trust policy.
4. The workflow runs Terraform format, validation, and plan.
5. A reviewed apply workflow can deploy the selected Atmos component.

## Why OIDC

OIDC avoids storing long-lived AWS access keys in GitHub secrets. Access is granted at runtime and should be scoped to:

- GitHub organization or user
- Repository name
- Branch or environment
- Required AWS permissions only

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
