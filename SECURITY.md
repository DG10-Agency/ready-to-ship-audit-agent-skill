# Security Policy

## Report only

This skill is read-only by design. It does not change code, config, tags,
deploys, migrations, or CI. Do not use it to apply fixes unattended.

## Report a vulnerability

Open a GitHub issue titled `[SECURITY]` with the affected file and version.
Do not include secrets, tokens, customer data, or production credentials in
the report. Expect triage within 7 days.

## Authorized staging

Run gates against staging or local clones only. Never point evidence
collection at production data stores unless explicitly authorized, and never
exfiltrate secrets encountered during a sweep.

## Redact secrets

Redact API keys, tokens, passwords, and connection strings from reports,
fix plans, logs, and pasted command output before sharing.
