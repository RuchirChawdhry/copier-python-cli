# copier-python-cli

A lean, reusable Copier template for agent-ready Python CLI applications. ⚡

**Stack:** uv · Python 3.14.7 · Cyclopts · ruamel.yaml · Rich · Ruff · pytest.

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
- Rich terminal output plus a safe ruamel.yaml config reader and sample YAML.
- Real pytest tests for logic and CLI, Ruff formatting/lint settings, `.python-version`.
- `AGENTS.md` with repo-local TDD and agent-environment guidance.
- PR-only GitHub Actions callers for the central **python-cli** and **python-build** workflows.
- MIT license, `.gitignore`, Copier answers for future `copier update`.

## Why the template repo never runs these workflows

The workflow source lives in `template/.github/workflows/ci.yml.jinja`, **not**
`.github/workflows/` at this repository's root. GitHub only detects workflows in the
root `.github/workflows/`, so nothing is activated here. Copier emits the normal
`.github/workflows/ci.yml` only into generated projects. Generated workflows run on
**pull requests only**, never `push`, `schedule`, or manual dispatch.

The CI jobs reference:

- [`python-cli.yml`](https://github.com/RuchirChawdhry/ci-workflows/blob/main/.github/workflows/python-cli.yml) for uv, Ruff, pytest, and help smoke test.
- [`python-build.yml`](https://github.com/RuchirChawdhry/ci-workflows/blob/main/.github/workflows/python-build.yml) for wheel/sdist validation and CLI installation smoke test.

They currently follow the `main` branch. Pin to a release tag or commit SHA if strict
reproducibility is required; the user-managed central workflows remain the source of truth.

## Test this template itself

```sh
uv run --no-project --with copier --with pytest pytest tests -q
```

The tests generate a sample application and assert package metadata, imports,
Copier update context, and isolated PR-only workflow placement. No GitHub Actions
workflows are registered in this template repository.

## Philosophy

**Less setup. More building.** Keep the template small, projects isolated, and agents
focused on tests and working software.
