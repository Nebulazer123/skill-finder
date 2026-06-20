# Devin Codex Setup

Use when Skill Finder needs DeepWiki plus Devin inside Codex.

## Codex MCP Config

Add DeepWiki and Devin to `~/.codex/config.toml`:

```toml
[mcp_servers.deepwiki]
url = "https://mcp.deepwiki.com/mcp"

[mcp_servers.deepwiki.tools.read_wiki_structure]
approval_mode = "approve"

[mcp_servers.deepwiki.tools.read_wiki_contents]
approval_mode = "approve"

[mcp_servers.deepwiki.tools.ask_question]
approval_mode = "approve"

[mcp_servers.devin]
url = "https://mcp.devin.ai/mcp"
bearer_token_env_var = "DEVIN_API_KEY"
env_http_headers = { "X-Org-Id" = "DEVIN_ORG_ID" }
startup_timeout_sec = 30
tool_timeout_sec = 600

[mcp_servers.devin.tools.read_wiki_structure]
approval_mode = "approve"

[mcp_servers.devin.tools.read_wiki_contents]
approval_mode = "approve"

[mcp_servers.devin.tools.ask_question]
approval_mode = "approve"

[mcp_servers.devin.tools.list_available_repos]
approval_mode = "approve"

[mcp_servers.devin.tools.list_integrations]
approval_mode = "approve"

[mcp_servers.devin.tools.devin_session_search]
approval_mode = "approve"

[mcp_servers.devin.tools.devin_session_events]
approval_mode = "approve"
```

Session creation and playbook/knowledge tools can be enabled per run when a task needs them; see the Deep Stress Pattern below.

## Environment

Set the local environment values before starting Codex:

```bash
launchctl setenv DEVIN_API_KEY "<your-devin-token>"
launchctl setenv DEVIN_ORG_ID "<your-devin-org-id>"
```

For terminal-only Codex runs, shell exports also work. Use your shell's normal environment-variable syntax and avoid pasting real tokens into shared logs:

```bash
export DEVIN_API_KEY
export DEVIN_ORG_ID
```

## Verification

Check config without printing the token:

```bash
codex mcp get devin
printf 'DEVIN_API_KEY length: '; launchctl getenv DEVIN_API_KEY | awk '{print length($0)}'
```

Fresh-session smoke. Start Codex from a shell where the Devin environment values are already present:

```bash
codex exec --skip-git-repo-check --sandbox read-only --ephemeral \
  "Use only read-only MCP calls. Ask DeepWiki one source-path question about vllm-project/vllm. Then call Devin list_integrations or list_available_repos and summarize only broad counts/status categories."
```

Passing setup means Codex exposes `deepwiki` and `devin`, DeepWiki `ask_question` completes, and one read-only Devin call completes.

## Deep Stress Pattern

Use this when Skill Finder needs evidence that Devin can do more than list integrations.

Run one bounded session against a public repo with a file-level question, poll until Devin returns a useful answer or the timebox expires, then terminate the session. Keep the prompt narrow enough that the expected answer can be scored by source paths.

Example scoring target:

- repo: `vllm-project/vllm`
- question: trace `POST /v1/chat/completions` from request schema through serving and engine generation
- pass threshold: at least six relevant source paths plus unresolved uncertainty checks

For temporary terminal runs, enable the session tools only for that command. Start from a shell where the Devin environment values are already present:

```bash
codex exec --skip-git-repo-check --sandbox read-only --ephemeral \
  -c 'mcp_servers.devin.tools.devin_session_create.approval_mode="approve"' \
  -c 'mcp_servers.devin.tools.devin_session_interact.approval_mode="approve"' \
  -c 'mcp_servers.devin.tools.devin_session_search.approval_mode="approve"' \
  -c 'mcp_servers.devin.tools.devin_session_events.approval_mode="approve"' \
  "Create one Devin session for vllm-project/vllm, ask for a file-level chat-completions trace, poll for the answer, summarize source paths, and terminate the session."
```
