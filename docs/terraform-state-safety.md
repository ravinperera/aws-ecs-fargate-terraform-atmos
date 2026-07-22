# Terraform State Safety

Terraform state is operationally sensitive. It can contain resource identifiers, topology details, and values returned by providers. Treat it as controlled infrastructure data rather than a normal build artifact.

## Recommended baseline

- Store state in a remote backend; do not rely on an engineer's local filesystem.
- Encrypt state at rest and in transit.
- Restrict backend access to the deployment role and a small break-glass administrator group.
- Enable state locking or the backend's equivalent concurrency protection.
- Enable versioning and retention so an earlier state version can be recovered.
- Log backend access and alert on unusual reads, deletes, or policy changes.

## Environment isolation

Use a separate state key or backend boundary for each environment and region. Production state should not share credentials or write permissions with development workflows.

A practical naming convention is:

```text
<service>/<environment>/<region>/terraform.tfstate
```

Atmos stack names and backend keys should describe the same environment. Review both when copying or renaming stacks to avoid applying a plan against the wrong state.

## Locking and concurrent runs

Only one apply operation should be allowed against a state object at a time. CI workflows should also use GitHub Actions concurrency groups so duplicate runs do not race before Terraform acquires the backend lock.

Never force-unlock state until you have confirmed:

1. No apply process is still running.
2. The lock owner and timestamp are understood.
3. The interrupted run's logs have been reviewed.
4. A fresh plan will be generated after unlocking.

## Safe state migration

Before moving or renaming a backend:

1. Pause automated plans and applies.
2. Capture the current state version and backend configuration.
3. Back up the state through the backend's supported mechanism.
4. Test access to the destination with least-privilege credentials.
5. Use Terraform's supported backend migration flow rather than copying files manually.
6. Run `terraform plan` and confirm that no unexpected resource replacement is proposed.
7. Re-enable automation only after the new backend and lock behaviour are verified.

## Recovery

If state is deleted or corrupted, stop all applies. Restore the most recent known-good version, then run a refresh-only plan or an equivalent read-only reconciliation before making changes. Do not import or recreate resources blindly; first establish which resources still exist and which state version represents the last successful deployment.

Document the recovery decision, restored version, validation output, and any drift discovered.