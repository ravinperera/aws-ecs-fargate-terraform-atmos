# Deployment Readiness Checklist

Use this checklist before adapting the reference pattern for a real ECS Fargate workload. It is intentionally conservative: completing it does not replace an architecture, security, or change review.

## 1. Replace Reference Values

- [ ] Replace the example AWS account ID and GitHub OIDC role ARN.
- [ ] Replace placeholder VPC, private subnet, security group, cluster, target group, IAM role, log group, and image values.
- [ ] Confirm the selected Atmos stack matches the intended account, environment, and AWS Region.
- [ ] Use an immutable image tag, such as a release version or commit SHA; do not use `latest`.
- [ ] Commit a reviewed provider lock file if this pattern is converted into a deployable module.

## 2. Identity and Permissions

- [ ] Restrict the GitHub OIDC trust policy to the expected repository, branch or environment, and workflow context.
- [ ] Grant the deployment role only the actions and resources required by Terraform and the release process.
- [ ] Keep the ECS task execution role separate from the application task role.
- [ ] Confirm the task role grants only the runtime permissions needed by the application.
- [ ] Protect production GitHub environments with required reviewers and deployment rules.

## 3. Network and Load Balancing

- [ ] Place tasks in private subnets and keep `assign_public_ip = false` unless there is a documented exception.
- [ ] Confirm private subnets have the required NAT gateway or VPC endpoints for ECR, CloudWatch Logs, Secrets Manager, and application dependencies.
- [ ] Restrict the task security group to required ingress from the load balancer and required egress destinations.
- [ ] Confirm the target group health-check path, matcher, interval, and grace period suit the application.
- [ ] Validate DNS, TLS certificates, listener rules, and web application firewall controls where applicable.

## 4. Secrets and Application Configuration

- [ ] Store secrets in AWS Secrets Manager or Parameter Store rather than plaintext stack files or GitHub variables.
- [ ] Confirm the task execution role can read only the referenced secrets.
- [ ] Keep non-sensitive environment variables separate from secrets.
- [ ] Verify that logs, error messages, and health endpoints do not expose sensitive values.
- [ ] Define a process for secret rotation and emergency revocation.

## 5. Reliability and Observability

- [ ] Choose CPU, memory, desired count, and autoscaling thresholds from load-test or production evidence.
- [ ] Set CloudWatch log retention to meet operational and compliance requirements.
- [ ] Configure alarms for unhealthy tasks, deployment failures, target health, CPU, memory, and application error rates.
- [ ] Confirm dashboards and alerts identify the service, environment, Region, and release version.
- [ ] Decide whether ECS Exec is required; disable it when it is not needed, or tightly control and audit access when enabled.

## 6. Plan and Change Review

- [ ] Run `terraform fmt -check -recursive`.
- [ ] Run Atmos component validation for the selected stack.
- [ ] Review the Terraform plan for replacements, public exposure, IAM expansion, security-group widening, and data-impacting changes.
- [ ] Have a second reviewer approve production-impacting infrastructure changes.
- [ ] Record the approved plan or change reference where required by the organisation's change process.

## 7. Rollout and Rollback

- [ ] Confirm the previous task definition and container image remain available.
- [ ] Define rollback triggers, the person responsible for the decision, and the rollback command or workflow.
- [ ] Use deployment circuit breakers, health-check grace periods, and rolling deployment settings appropriate to the service.
- [ ] Avoid schema changes that prevent the previous application version from starting.
- [ ] Schedule higher-risk production changes within a supported change window.

## 8. Post-Deployment Verification

- [ ] Confirm the ECS service reaches a steady state with the expected number of healthy tasks.
- [ ] Verify the running task definition and image digest match the approved release.
- [ ] Test the load balancer health endpoint and one representative application request.
- [ ] Check CloudWatch Logs, alarms, target health, and deployment events for errors.
- [ ] Confirm no unexpected public IPs, security-group rules, IAM permissions, or secret values were introduced.
- [ ] Record the deployment outcome and any follow-up actions.

## Reference Pattern Boundary

This repository demonstrates structure and conventions. A production implementation still needs organisation-specific account vending, remote state, locking, policy enforcement, autoscaling, disaster recovery, cost controls, compliance evidence, and incident procedures.
