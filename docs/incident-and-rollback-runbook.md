# ECS Deployment Incident and Rollback Runbook

Use this runbook when a deployment causes failed tasks, unhealthy targets, elevated errors, latency, or dependency pressure.

## Stop conditions

Pause the rollout and start incident handling when any agreed service objective is breached, the ECS deployment circuit breaker activates, healthy target count falls below the safe minimum, error rate rises materially, or the new task revision cannot reach steady state.

Do not keep retrying the same deployment without understanding the failure. Repeated starts can amplify load on databases, queues, secrets endpoints, and external services.

## Capture evidence first

Record:

- incident start time and deployment workflow URL;
- previous and new task definition revisions;
- image digest and release identifier;
- ECS service events and stopped-task reasons;
- target group health reasons;
- application and FireLens/OpenTelemetry logs where configured;
- CPU, memory, request count, latency, error rate, queue depth, and dependency health;
- Terraform plan/apply output and any manual console action.

Preserve evidence without copying secrets, tokens, personal data, or full production payloads into issues or chat.

## Triage sequence

1. Confirm whether the failure affects all tasks, only the new revision, or a dependency shared by both revisions.
2. Check task placement, subnet IP capacity, security groups, execution-role access, image pull, secrets retrieval, health-check path, and container port.
3. Compare the new task definition with the last known-good revision.
4. Check ALB target health and whether health-check grace and deregistration settings match application startup and shutdown behaviour.
5. Validate database, cache, queue, DNS, and third-party dependency health before assuming the container is the root cause.

## Rollback options

Choose the smallest reliable rollback:

- redeploy the last known-good task definition revision;
- restore the previous immutable image digest;
- revert the infrastructure commit and apply the reviewed rollback plan;
- disable a new feature through an existing, tested feature flag;
- reduce desired count only when excess capacity itself is causing dependency pressure.

Avoid editing task definitions or networking manually unless the approved recovery procedure requires it. If an emergency console change is unavoidable, record it immediately and reconcile it back into Terraform after stability returns.

## Post-rollback verification

Confirm all of the following before closing the incident:

- ECS service reaches steady state with the expected task revision;
- target group healthy count and availability return to normal;
- application errors, latency, saturation, and queue age recover;
- no tasks remain repeatedly stopping or pending;
- database connections and downstream limits return to safe levels;
- alarms clear for the right reason, not because telemetry stopped;
- a representative user or synthetic transaction succeeds.

## Follow-up

Create a corrective issue that captures root cause, missing detection, why pre-production validation did not catch the problem, and the preventive control. Update tests, alarms, deployment gates, or documentation rather than relying only on operator memory.