## Summary

What changed and why?

## Validation

- [ ] `python3 -m unittest discover -s validation -v`
- [ ] Skill validator, if available
- [ ] Public scan for private paths, secrets, and raw workspace artifacts

## Safety Review

- [ ] No credentials, private paths, raw chats, or private workspace files added
- [ ] Install commands are source-backed or marked not verified
- [ ] Approval boundaries for installs, credentials, risky scripts, and global mutation are preserved

## Notes

Anything reviewers should inspect closely?
