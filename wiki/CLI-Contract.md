# CLI contract

Use the same interface for people and automation. Every starter application subcommand and the root configuration actions accept shared output options.

| Flag | Effect |
| --- | --- |
| --json | One compact JSON document |
| --jsonl | One record per line; an empty list emits nothing |
| --quiet | Suppress progress and console diagnostics, retain results and errors |
| --verbose | Debug console logs for business commands, verbose diagnostic notes |

JSON and JSONL are mutually exclusive; quiet and verbose are mutually exclusive. Machine output is UTF-8 with trailing newlines, no ANSI formatting or progress. Results go to stdout; logs, progress and errors go to stderr. Help and parse errors remain textual.

```sh
uv run my-tool hello --name Ada --json
uv run my-tool doctor --json
uv run my-tool db-path --json
uv run my-tool db-list --jsonl
```

Doctor checks Python, platform, YAML settings, config/log/database paths and SQLite. It returns status 1 for failed checks, after emitting results. Its database check reads an on-disk immutable snapshot, not live WAL state. db-path does not initialize the database; db-list may initialize it and returns records sorted by key.

## Implement new commands

Reuse the existing immutable default output options rather than constructing an object in a function signature. Create Output(options), call domain logic and use output.emit(data). Use output.track() or output.progress() for progress. Do not implement separate serializers.

Raise ApplicationError for expected domain failures. The main boundary handles expected application, filesystem, SQLite, Unicode and YAML errors; unexpected programming failures propagate. Cyclopts owns parsing and argument validation. Do not duplicate error handling in each command.
