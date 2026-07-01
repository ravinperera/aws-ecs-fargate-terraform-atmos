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

Examples:

```bash
terraform fmt -recursive
atmos terraform validate aws/ecs-fargate-service -s dev/eu-west-2
atmos terraform plan aws/ecs-fargate-service -s dev/eu-west-2
```

If validation was not run, explain why.

## Notes

Add any assumptions, screenshots, links, or follow-up items.
