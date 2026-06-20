# Security Policy

## Supported Versions

Security fixes are made on the default branch and included in the next tagged release. Older tags are preserved for reproducibility but are not separately maintained.

## Reporting a Vulnerability

Use GitHub-native reporting for this repository.

If GitHub Security Advisories are enabled, open a private vulnerability report through GitHub. If private advisories are not available, open a public issue with only a minimal summary and no exploit details, secrets, tokens, or private data. A maintainer can then arrange the safest follow-up path.

Include the affected file or route, the public-safe reproduction steps, the expected behavior, the observed behavior, and any relevant tool versions. Do not include real credentials, private repository contents, private prompts, raw chat logs, or sensitive local paths.

## Scope

Please report issues that could cause Skill Finder to:

- expose secrets or private paths
- run candidate scripts without approval
- install or mutate global state without approval
- recommend unsafe commands as verified
- blur the boundary between source evidence and executable instructions
- misrepresent required setup for MCP servers, plugins, CLIs, or package dependencies
- package stale plugin files that differ from the canonical skill

Out of scope: vulnerabilities in third-party services, MCP servers, plugins, packages, or hosted platforms that Skill Finder only links to. Report those issues to the upstream project unless Skill Finder documents the unsafe behavior as verified or safe.

## Handling

Maintainers will triage reports on a best-effort basis, patch public documentation or validation when needed, and add regression coverage for confirmed issues. If a report concerns a third-party command, dependency, or integration, the fix may be to mark the command unverified, change setup guidance, or point users to upstream guidance.

## Safety Notes

Do not include real credentials, private repository contents, or sensitive logs in public issues. Redact local paths and tokens before sharing reproduction details. Do not test Skill Finder against systems or repositories you do not have permission to inspect.
