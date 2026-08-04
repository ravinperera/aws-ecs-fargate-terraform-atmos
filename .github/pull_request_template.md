## Summary

- 

## Type of Change

- [ ] Documentation update
- [ ] Terraform component change
- [ ] Atmos stack example change
- [ ] GitHub Actions or CI/CD change
- [ ] Operational guidance update

## Review Checklist

- [ ] README or docs updated when behaviour or structure changed
- [ ] Placeholder values remain generic
- [ ] Terraform and Atmos examples remain environment-neutral
- [ ] IAM, networking, logging, and secret-handling implications considered
- [ ] Deployment and rollback impact considered where relevant

## Validation

Describe what was checked.

Credential-free examples:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/check_markdown_links.py .
terraform -chdir=infrastructure/components/terraform/aws/ecs-fargate-service fmt -check -recursive
cd infrastructure
atmos validate stacks
terraform -chdir=components/terraform/aws/ecs-fargate-service init -backend=false -input=false
terraform -chdir=components/terraform/aws/ecs-fargate-service validate
```

Authenticated plan example after replacing placeholders:

```bash
cd infrastructure
atmos terraform plan aws/ecs-fargate-service -s eu-west-2
```

If validation was not run, explain why.

## Notes

Add any assumptions, screenshots, links, or follow-up items.
