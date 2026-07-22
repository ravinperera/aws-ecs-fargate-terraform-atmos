# ECS Scaling and Cost Guardrails

Scaling policy should protect availability without allowing a noisy workload or bad metric to create unbounded capacity and spend.

## Start with measured task sizing

Choose Fargate CPU and memory from observed workload behaviour rather than copying a convenient default. Run representative load tests and record:

- steady-state and peak CPU utilisation;
- memory working set and out-of-memory events;
- request latency and queue depth;
- startup time and health-check stabilisation time;
- downstream limits such as database connections.

Leave deliberate headroom, but investigate consistently low utilisation instead of treating over-provisioning as permanent safety capacity.

## Autoscaling baseline

Define explicit minimum, desired, and maximum task counts for every environment. Production minimum capacity should tolerate the loss or replacement of one task where availability requires it. Maximum capacity must reflect downstream limits and an accepted cost ceiling.

Use service-level demand signals where possible:

- ALB request count per target for request-driven services;
- queue depth or age for asynchronous workers;
- CPU for compute-bound workloads;
- memory only when it reliably tracks demand.

Avoid scaling solely from a noisy metric. Set cooldowns that account for task startup, load-balancer registration, and application warm-up.

## Safe scale-in

Scale-in is an availability event. Confirm that:

- deregistration delay allows in-flight requests to finish;
- application shutdown handles `SIGTERM` and stops accepting new work;
- queue workers extend visibility or return unfinished work safely;
- deployment and autoscaling policies do not remove capacity simultaneously;
- minimum healthy percentage preserves enough serving tasks.

## Cost controls

- Use immutable image tags so rollback and cost analysis refer to a known release.
- Apply AWS Budgets or equivalent alerts before production adoption.
- Tag services, tasks, log groups, and supporting resources with owner, environment, and cost centre.
- Set CloudWatch Logs retention explicitly.
- Review NAT Gateway, data transfer, load balancer, log ingestion, and OpenTelemetry costs; Fargate task cost is only one part of the service.
- Consider Fargate Spot only for interruption-tolerant workloads with tested recovery behaviour.

## Warning signs

Investigate when any of these persist:

- task count remains at maximum capacity;
- CPU is low while latency or queue age is high;
- frequent scale-out and scale-in oscillation occurs;
- memory steadily rises between deployments;
- desired tasks cannot start because of subnet IP, quota, image-pull, or IAM failures;
- cost grows faster than request volume;
- log or telemetry ingestion dominates compute cost.

## Review record

For each scaling change, record the metric, target value, min/max capacity, expected cost range, downstream constraint, validation period, rollback value, and owner. Revisit the policy after major traffic, code, task-size, or dependency changes.