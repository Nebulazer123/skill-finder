## Summary

What changed and why?

## Validation

- [ ] `python3 -m unittest discover -s skills/skill-finder/tests -v`
- [ ] `python3 -m unittest discover -s validation -v`
- [ ] `python3 -m unittest discover -s evaluation -v`
- [ ] `python3 scripts/sync_plugin_package.py --check`
- [ ] `npm ci --ignore-scripts`
- [ ] `npm ls --all`
- [ ] Skill validator, if available
- [ ] Public scan for private paths, secrets, and raw workspace artifacts

## Safety Review

- [ ] No credentials, private paths, raw chats, or private workspace files added
- [ ] Install commands are source-backed or marked not verified
- [ ] Task-specific route/setup changes are reflected in README, skill docs, plugin package, and tests
- [ ] Generated or community sources are not sole proof for material claims
- [ ] Failed/cancelled route cases recover through a different source family
- [ ] Approval boundaries for installs, credentials, risky scripts, and global mutation are preserved

## Notes

Anything reviewers should inspect closely?
