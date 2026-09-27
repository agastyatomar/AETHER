# Security Policy

## Scope

AETHER is an alpha project that can execute tools, browser actions, subprocesses, and agent workflows. Treat deployments as security-sensitive.

## Supported versions

Only the latest `main` branch and the newest published release receive active security fixes.

## Reporting

Please report suspected vulnerabilities privately through GitHub's private security reporting mechanism when available. Do not publish credentials, tokens, private data, or exploit details in a public issue.

Include:
- affected commit or version;
- reproducible steps;
- expected and observed behavior;
- impact and affected component.

## Deployment guidance

- Do not expose the web API directly to the public internet without an authentication and network boundary.
- Set `AETHER_DEMO_MODE=1` for public demonstrations; this disables `/api/run` and `/api/command` execution.
- Keep agent capabilities minimal and review skills, plugins, MCP servers, browser permissions, and credentials before enabling them.
- Run browser automation and untrusted tools in a sandbox or isolated container where practical.
- Never commit API keys, cookies, tokens, or production credentials.
- Prefer dedicated test accounts with minimum permissions.

Security controls reduce risk but do not guarantee a safe deployment. AETHER remains alpha software.
