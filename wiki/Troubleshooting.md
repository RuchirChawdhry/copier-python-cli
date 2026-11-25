# Troubleshooting

| Symptom | Action |
| --- | --- |
| CLI command not found | Run uv sync --group dev, then uv run my-tool --help. For a standalone command run task install and reopen the shell. |
| Commit stopped after formatting | Inspect git diff, stage the intended changes again and retry the commit. |
| Hooks not installed | Initialize Git at the project root and rerun task setup. |
| Focused tests miss a change | Run task test:all, especially for subprocess or external changes. |
| JSON parsing fails | Remove incompatible flags; parse stdout only, and check stderr and exit status. |
| Invalid YAML or named logging level | Inspect --show-config or the error details, correct the file, and run doctor. |
| Config initialization fails | Check --config-path; an existing file is deliberately not overwritten. |
| SQLite schema or path problem | Run doctor --json, verify the local storage path and schema version; do not delete a user's data as a repair. |
| Shared CI failure | Inspect the failing job and its central workflow; reproduce the relevant validation locally before changing code. |

Useful commands:

```sh
uv run my-tool doctor --json
uv run my-tool --config-path
uv run my-tool db-path
uv run ruff check .
uv run pytest -q
```

See [Wiki publishing](Wiki-Publishing) for documentation sync issues.
