# Security Policy

## Supported Scope

Security reports are welcome for the current `main` branch, including the Terraform examples, Atmos configuration, GitHub Actions workflows, documentation, and helper scripts.

This repository is a public reference implementation. It does not operate a hosted service, manage a production AWS account, or provide credentials. Security findings should therefore focus on unsafe patterns, misleading guidance, exposed sensitive data, or vulnerabilities in repository-owned code and configuration.

## Reporting a Vulnerability

Please do not publish exploit details, credentials, AWS account identifiers, private infrastructure information, or client data in a public issue.

Use GitHub's private vulnerability reporting option from the repository's **Security** tab when it is available. If private reporting is unavailable, open a minimal public issue asking the maintainer to establish a private contact channel. Include no sensitive technical detail in that issue.

A useful private report should include:

- the affected file, workflow, or example;
- the security impact and realistic misuse scenario;
- safe reproduction steps using fictional values;
- any suggested mitigation;
- whether sensitive data may already be exposed.

Reports are reviewed on a best-effort basis. Please allow time for validation before public disclosure.

## Accidentally Exposed Credentials

If a credential, token, private key, account identifier, or sensitive endpoint is committed:

1. Revoke or rotate the credential immediately.
2. Review provider and GitHub audit logs for unexpected use.
3. Remove the value from the current branch and repository history where appropriate.
4. Replace it with a clearly fictional placeholder.
5. Do not assume deleting the latest commit makes the secret safe.

Never test a report against infrastructure you do not own or have explicit permission to assess.

## Out of Scope

The following are normally out of scope unless they expose a repository-specific security problem:

- vulnerabilities in AWS, Terraform, Atmos, GitHub Actions, or third-party actions themselves;
- attacks that require access to a real environment not provided by this repository;
- generic hardening suggestions without a concrete issue in the example;
- availability or service-level concerns for a hosted system, because no hosted system is operated here.

For third-party vulnerabilities, report them to the relevant upstream project through its security process.
