# copier-python-cli

A minimal, agent-ready **Copier template for Python CLI apps**, powered by **uv**, **Cyclopts**, **Rich**, **Ruff**, and **pytest**. Fast to bootstrap, easy to extend, and test-first by default.

## Generate a new CLI

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run:

```sh
uvx --from copier copier copy gh:RuchirChawdhry/copier-python-cli ./my-cli
cd my-cli
uv sync
uv run my-cli --help
uv run my-cli greet Ada
```

`my-cli` in these examples assumes you enter `my-cli` as the project name when prompted. Copier asks for the CLI name, description, author and Python version. The name determines both the installed command (`my-cli`) and importable Python package (`my_cli`). No package-manager choices or post-generation hooks to maintain.

## Generated project

```text
my-cli/
├── .github/workflows/ci.yml
├── .copier-answers.yml
├── .gitignore
├── .python-version
├── AGENTS.md
├── LICENSE
├── README.md
├── pyproject.toml
├── src/my_cli/
│   ├── __init__.py
│   ├── __main__.py
│   └── cli.py
└── tests/test_cli.py
```

### Daily commands

| Task | Command |
| --- | --- |
| Install dependencies | `uv sync` |
| Run CLI | `uv run my-cli --help` |
| Add runtime dependency | `uv add <package>` |
| Add development dependency | `uv add --dev <package>` |
| Test | `uv run pytest -q` |
| Lint | `uv run ruff check .` |
| Format | `uv run ruff format .` |
| Build | `uv build` |

The generated project installs itself as a package using `uv_build` with a `src/` layout. Its GitHub Actions workflow runs quality checks on pull requests and pushes to `main`.

## Test the template itself

```sh
uv run --no-project --with copier --with pytest pytest tests -q
```

The template tests generate temporary projects, inspect metadata and file names, and exercise `uv sync`, Ruff, pytest, the installed CLI, and `uv build`. The checks also run automatically in this repository's pull requests.

## Updating generated projects

Commit `.copier-answers.yml` and `uv.lock` in each generated application. Once this template has versioned release tags, run `copier update` inside a generated project to incorporate template improvements while retaining project changes.

## License

MIT. See [LICENSE](LICENSE).
