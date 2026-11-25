# Development

Install uv and Go Task. Initialize Git before task setup so it installs pre-commit.

| Task | Purpose |
| --- | --- |
| task setup | Sync development dependencies and install hooks at Git root |
| task dev -- hello --json | Run a command in the development environment |
| task test | Focused tests using pytest-testmon |
| task test:all | Full tests and refresh selection baseline |
| task lint | Check Ruff lint and formatting |
| task fix | Apply safe lint fixes, format and recheck |
| task build | Build distribution artifacts |
| task install | Install user-level executable (uv preferred; pipx fallback) |
| task clean | Remove build artifacts and test/lint caches |
| task doctor -- --json | Diagnose environment |
| task update | Upgrade lockfile and sync dependencies |

## Git hooks

The local pre-commit hooks run the project's Ruff on staged Python files. The lint hook applies safe fixes (including import sorting through the I rule); the format hook formats code. If files change, review and stage them again before retrying the commit. Do not bypass hooks.

Run `uv run pre-commit run --all-files` for an explicit all-files pass. Ruff settings and version resolution are shared with normal development commands.

## Agent workflow

Read the generated AGENTS.md. Write a failing test for the behavior, implement the smallest passing change, then run task fix and task test. Before acceptance run task lint and task test:all. Keep logic in appropriate existing modules, avoid parallel infrastructure, prefer native Cyclopts parameter types and validators, and do not change shared CI or global Python environments from a generated project.
