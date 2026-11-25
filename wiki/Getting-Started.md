# Getting started

Install uv, Git and (for task shortcuts) [Go Task](https://taskfile.dev/docs/installation).

```sh
uvx copier copy gh:RuchirChawdhry/copier-python-cli my-tool
cd my-tool
git init
task setup
```

Choose My Tool / my-tool / my_tool / my-tool when prompted. Without Go Task, run `uv sync --group dev` and `uv run pre-commit install` after initializing Git.

## Copier answers

| Answer | Purpose | Example |
| --- | --- | --- |
| project_name | Display name | My Tool |
| project_slug | Distribution and storage name | my-tool |
| package_name | Python import name | my_tool |
| cli_command | Installed executable | my-tool |
| description | Package summary | A useful CLI |
| author_name | Copyright holder | Your name |

Slugs and executable names use lowercase letters, digits and single hyphens, starting with a letter. Package names permit underscores. Copier 9.14.1 or later is required.

For noninteractive generation:

```sh
uvx copier copy --defaults -d project_name='My Tool' gh:RuchirChawdhry/copier-python-cli my-tool
```

## Verify the project

```sh
uv run my-tool --help
uv run my-tool hello --name Ada --json
uv run my-tool doctor --json
task lint
task test:all
```

Expected greeting: `{"message":"Hello, Ada!"}`. Doctor returns nonzero if a check fails.

Commit the generated lockfile and Copier answers. To apply later template changes, work from a clean Git tree, review the selected template revision, and run `uvx copier update`. Copier updates can require conflict resolution; inspect the diff and run tests afterward.
