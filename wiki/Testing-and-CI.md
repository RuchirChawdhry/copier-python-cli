# Testing and CI

## Generated projects

```sh
task test
task test:all
task lint
task build
```

pytest-testmon uses observed Python execution to select affected tests. The first run establishes a baseline. Use the full suite for final acceptance and subprocess, external-resource or dynamic changes; focused selection cannot cover all such dependencies.

The generated PR-only workflow calls python-cli.yml and python-build.yml in the [central workflow repository](https://github.com/RuchirChawdhry/ci-workflows). It currently passes Python 3.14.7 and the configured CLI command and references the central main branch. Pin workflow revisions if stricter reproducibility is required.

## Template repository

```sh
uv run --no-project --with copier==9.14.1 --with pytest --with PyYAML pytest tests/test_template.py -q
```

The root PR-only Template CI calls the central copier-ci.yml workflow. It checks the template contracts, renders a project, validates lint and tests, builds distributions and performs installed-wheel functional checks on Ubuntu 24.04.

The functional smoke suite in tests/smoke_installed.py expects CLI_EXECUTABLE to point to an installed console script. It checks actual JSON output, configuration precedence, malformed YAML diagnostics, SQLite WAL, and read-only doctor behavior outside the generated source tree. It is intended to run with an installed wheel, not as an ordinary standalone test without that environment.

The generated workflow lives under template/.github/workflows; GitHub does not activate it in the template repository. The wiki publisher is separate from both CI workflows.
