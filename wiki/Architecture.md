# Architecture

The repository has two scopes: root files maintain and test the template, while Copier renders only `template/`. Generated applications have their own isolated dependencies and CI.

| Generated file | Responsibility |
| --- | --- |
| src/my_tool/cli.py | Cyclopts commands and centralized error handling |
| src/my_tool/__main__.py | Module entrypoint |
| src/my_tool/config.py | Safe YAML settings, platform paths, Loguru setup |
| src/my_tool/output.py | Shared output options, JSON/JSONL, Rich progress |
| src/my_tool/database.py | SQLite connection, schema and record API |
| src/my_tool/doctor.py | Read-only environment checks |
| src/my_tool/logging_utils.py | Optional synchronous call tracing |
| src/my_tool/errors.py | Expected application failures |
| pyproject.toml | Package metadata, entrypoint, dependency and tool configuration |
| Taskfile.yml | Repeatable development commands |
| AGENTS.md | Project-local development instructions |
| tests/ | CLI and component regression tests |

The console entrypoint and module entrypoint invoke `cli.main()`. Keep business logic outside CLI handlers. Commands validate arguments via Cyclopts, call domain functions, then emit data through the existing Output class.

## Persistence boundaries

Use YAML for configuration and SQLite for application data. Use platformdirs for per-user paths rather than the current working directory. The starter SQLite schema is version 1 with a key/value records table. Extend it with explicit migrations and project-specific operations. Parameterize queries and reuse `database.connect()`; it enables WAL and foreign keys, commits or rolls back transactions, and closes connections.

SQLite initializes lazily. Help, config and doctor do not initialize it; db-list does. Keep WAL databases on a local filesystem and use a proper SQLite backup mechanism for live data.

## Packaging

uv_build produces a wheel and source distribution. The project starts at version 0.1.0; the runtime requires Python >=3.14, and the development interpreter is pinned to 3.14.7.
