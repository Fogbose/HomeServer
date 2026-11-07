# Contributing

Small, focused pull requests are welcome. Explain the problem, changed behavior,
tests and limits. Use an issue for reproducible bugs or a feature proposal, but
do not report security vulnerabilities publicly; read [SECURITY](SECURITY.md).

## Development

Python 3.10+ and Git are enough for helper development:

```sh
python3 -m unittest discover -s tests -v
```

For Compose changes, use a disposable Linux Docker host, initialize fresh
credentials, run `docker compose config -q`, start the stack and check status,
cron, files and persistence. Never test a PR with your personal live data.
Docker integration testing downloads pinned upstream images and creates volumes.
Do not approve a change based solely on passing Python mocks.

Keep helpers dependency-free where practical. Validate input, propagate errors,
avoid logging secrets, and prefer preview/read-only behavior. Destructive actions
need explicit scope and confirmation and do not belong in a default setup path.
Document OS, shell, privileges and rollback for operational changes.

Use English for shared code/main documentation; French contributions are welcome
and can be translated during review. Keep README.fr.md synchronized when changing
its quick start. Use meaningful commit messages; there is no mandatory signing
or external contributor agreement configured. Contributions are under MIT.

Be respectful: discuss technical behavior, acknowledge uncertainty and avoid
personal attacks, harassment or sharing personal information. No response-time
commitment or dedicated moderation team is promised.
