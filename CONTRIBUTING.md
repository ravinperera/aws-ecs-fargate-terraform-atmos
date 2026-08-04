# Contributing

Thanks for improving this ECS Fargate Terraform Atmos reference pattern.

This repository is intentionally generic. Contributions should keep it useful as a public example without adding company-specific infrastructure, account IDs, secrets, or client data.

## Good Contribution Areas

Useful changes include:

- clearer README or documentation examples
- safer Terraform defaults or validation notes
- Atmos stack examples that explain environment-specific inputs
- GitHub Actions improvements for review, plan, or deployment safety
- IAM, networking, secrets, logging, and rollback guidance
- small refactors that make the reference easier to understand

## Before Opening a PR

Please check that your change:

- keeps placeholder values generic
- avoids real AWS account IDs, ARNs, domains, IP ranges, credentials, or client names
- explains any security-sensitive behaviour such as IAM permissions, network exposure, secrets, or deployment access
- keeps reusable Terraform logic separate from environment-specific Atmos stack values
- updates the README or docs when the repository layout or usage changes

## Security Reports

Do not use a public issue or pull request to disclose credentials, private infrastructure details, client data, exploit steps, or an unpatched vulnerability. Follow the [security policy](SECURITY.md) and use private vulnerability reporting when available.

## Terraform and Atmos Changes

For Terraform or Atmos examples, include enough context for someone to understand the intent without assuming access to a real AWS account.

Where possible, mention the validation you performed, such as:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/check_markdown_links.py .
terraform -chdir=infrastructure/components/terraform/aws/ecs-fargate-service fmt -check -recursive
cd infrastructure
export ATMOS_STACKS_NAME_PATTERN='{environment}'
atmos terraform validate aws/ecs-fargate-service -s dev
atmos terraform plan aws/ecs-fargate-service -s dev
```

The first five commands are credential-free. A real plan requires AWS access and replacement of the repository's placeholder account and infrastructure values.

If a command cannot be run because the repository contains placeholder values, say that clearly in the PR notes.

## Pull Request Notes

A helpful PR should include:

- what changed
- why the change is useful
- which files or docs were updated
- what validation was run, or why validation was not applicable
- any security, IAM, networking, or secret-handling considerations

Keep changes small and reviewable where possible.
