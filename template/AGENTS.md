# Agent guide

This is a standalone **uv**-managed Python CLI. Do not mix its environment, dependencies, or commands with other repositories.

## Working contract

1. Follow red/green/refactor: add a failing pytest test, implement the smallest change, then refactor.
2. Keep the CLI layer thin (`src/*/cli.py`). Put reusable logic in importable modules and test it directly.
3. Run commands from this repository's root using `uv run` or `uv sync`. Never use system-wide `pip install` for project dependencies.
4. Avoid unrelated refactors or changes to sibling repositories. Add dependencies via `uv add` / `uv add --dev`.
5. Before finishing, run `uv run pytest -q`, `uv run ruff check .`, `uv run ruff format --check .`, and `uv build`.
6. Commit `uv.lock` after the first `uv sync` and whenever dependencies change.

## Layout

- `src/`: installable Python package and CLI entry point
- `tests/`: automated behavioral tests
- `pyproject.toml`: one source of truth for metadata, dependencies, tooling, and entry points
- `.github/workflows/ci.yml`: pull-request quality gate

Keep changes focused, readable, and portable across Windows, Linux, and macOS.
