# copier-python-cli

A lean, reusable Copier template for agent-ready Python CLI applications. ⚡

**Stack:** uv · Python 3.14.7 · Cyclopts · ruamel.yaml · Rich · platformdirs · Loguru · orjson · SQLite · Ruff · pytest · pytest-testmon · pre-commit · Go Task.

## Generate a project

```sh
uvx copier copy gh:RuchirChawdhry/copier-python-cli my-new-cli
cd my-new-cli
uv sync --group dev
uv run pytest -q
uv run ruff check .
uv run ruff format --check .
```

Copier prompts for project name, distribution/import names, CLI executable, description,
and author. Use `-d project_name='My Tool'` or `--defaults` for unattended setup.
Commit the generated `uv.lock` for reproducible development and CI.

## What's generated?

- Installable `src/` package using uv_build and an executable Cyclopts command.
- Rich terminal output, persistent per-user YAML settings via ruamel.yaml and platformdirs.
- Root configuration flags `--init-config`, `--config-path`, `--show-config` and the `set-config` subcommand; Loguru file/stderr logging with optional decorators.
- Read-only environment diagnostics, platform-aware SQLite persistence with WAL enabled by default and Rich progress reporting.
- Shared agent-friendly flags on all application subcommands: --json, --jsonl, --quiet, --verbose; machine output is compact UTF-8 serialized with orjson.
- Cross-platform Taskfile.yml with standardized development, focused/full testing, installation, cleanup and diagnostics tasks.
- Version-controlled pre-commit hooks for automatic Ruff lint fixes and formatting of staged Python files; installed by `task setup` after Git initialization.
- Real pytest tests for logic and CLI, Ruff formatting/lint settings, `.python-version`.
- `AGENTS.md` with repo-local TDD and agent-environment guidance.
- PR-only GitHub Actions callers for the central **python-cli** and **python-build** workflows.
- MIT license, `.gitignore`, Copier answers for future `copier update`.

## Continuous integration

This repository has a root workflow, `.github/workflows/template-ci.yml`,
which calls the central [Copier validation workflow](https://github.com/RuchirChawdhry/ci-workflows/blob/main/.github/workflows/copier-ci.yml).
It runs when a pull request is opened, updated or reopened. It tests the template
contracts, renders the current revision, runs Ruff and pytest on the generated
project, builds and checks distributions, and installs the wheel for functional smoke tests on Ubuntu 24.04.
The central workflow explicitly runs `tests/smoke_installed.py` against the
installed console script via `CLI_EXECUTABLE`, outside the generated project.
The tests cover machine output, configuration, SQLite WAL and doctor diagnostics. New commits cancel older runs for the same PR.

The generated application's independent workflow lives under
`template/.github/workflows/ci.yml.jinja`. Copier renders it into the generated
project; it is not run in this template repository. Generated workflows remain
PR-only.

The CI jobs reference:

- [`python-cli.yml`](https://github.com/RuchirChawdhry/ci-workflows/blob/main/.github/workflows/python-cli.yml) for uv, Ruff, pytest, and help smoke test.
- [`python-build.yml`](https://github.com/RuchirChawdhry/ci-workflows/blob/main/.github/workflows/python-build.yml) for wheel/sdist validation and CLI installation smoke test.

They currently follow the `main` branch. Pin to a release tag or commit SHA if strict
reproducibility is required; the user-managed central workflows remain the source of truth.

## Test this template itself

```sh
uv run --no-project --with copier==9.14.1 --with pytest --with PyYAML pytest tests -q
```

The tests generate a sample application and assert package metadata, imports,
Copier update context, and separation of the template-validation and generated-project
PR-only workflows.

## Philosophy

**Less setup. More building.** Keep the template small, projects isolated, and agents
focused on tests and working software.
