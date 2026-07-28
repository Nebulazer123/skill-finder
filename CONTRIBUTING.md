# Contributing

Thanks for improving Skill Finder. This repository is intentionally small: keep changes focused, source-backed, and easy for another agent or maintainer to inspect.

## Development Flow

1. Fork the repository.
2. Create a feature branch.
3. Make the smallest useful change.
4. Run validation from the repository root:

```bash
python3 -m unittest discover -s skills/skill-finder/tests -v
python3 -m unittest discover -s validation -v
python3 -m unittest discover -s evaluation -v
python3 scripts/sync_plugin_package.py --check
npm ci --ignore-scripts
npm ls --all
```

5. If you have access to a Codex skill validator, also run:

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py skills/skill-finder
```

6. If you changed `skills/skill-finder/`, sync the plugin package before opening a pull request:

```bash
python3 scripts/sync_plugin_package.py
```

7. Open a pull request with a short explanation, test results, and any approval or safety boundary affected by the change.

## Contribution Guidelines

- Do not add private paths, credentials, raw chat logs, local workspace notes, or unrelated examples.
- Keep the skill universal. Avoid tuning the public instructions to one person, one private use case, one company, or one local machine.
- Treat candidate install commands as evidence. Do not add guessed commands.
- Keep `package.json` limited to real npm-installable setup dependencies used by the README or skill docs.
- Keep public/local evaluation usable without accounts. Add connected routes as conditional capabilities with explicit data-classification handling.
- Preserve explicit approval before installs, credentials, risky scripts, publishing, paid execution, destructive actions, or persistent/global mutation.
- Treat generated summaries as leads. Add primary verification for every material recommendation claim.
- Add a different-family recovery case when introducing a route that can fail or be cancelled.
- Add or update validation when changing public package structure or safety boundaries.

## Useful Issue Reports

Please open an issue if you find stale source routes, broken install commands, risky candidate setup behavior, false setup blocks, biased recommendations, unclear approval boundaries, or a stronger evaluation scenario. Include the task prompt, sources searched if known, candidates returned, what seemed wrong, and any safer or stronger alternative.
