"""Copier-template contract tests. Run: uv run --no-project --with copier --with pytest pytest tests."""

import tomllib
from pathlib import Path

import pytest
import yaml
from copier import run_copy

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def generated(tmp_path: Path) -> Path:
    destination = tmp_path / "generated"
    run_copy(
        str(ROOT),
        destination,
        data={
            "project_name": "Sample CLI",
            "project_slug": "sample-cli",
            "package_name": "sample_cli",
            "cli_command": "sample-cli",
            "description": "A sample command line app.",
            "author_name": "Example Person",
        },
        defaults=True,
        vcs_ref="HEAD",
        unsafe=False,
    )
    return destination


def test_template_repo_workflow_calls_central_validation_only_on_pr() -> None:
    workflow = yaml.load(
        (ROOT / ".github" / "workflows" / "template-ci.yml").read_text(encoding="utf-8"),
        Loader=yaml.BaseLoader,
    )
    assert set(workflow["on"]) == {"pull_request"}
    assert set(workflow["on"]["pull_request"]["types"]) == {
        "opened", "synchronize", "reopened",
    }
    assert workflow["permissions"] == {"contents": "read"}
    assert workflow["jobs"]["validate"]["uses"] == (
        "RuchirChawdhry/ci-workflows/.github/workflows/copier-ci.yml@main"
    )
    assert (ROOT / "template" / ".github" / "workflows" / "ci.yml.jinja").exists()


def test_generated_package_metadata(generated: Path) -> None:
    with (generated / "pyproject.toml").open("rb") as stream:
        config = tomllib.load(stream)
    assert config["project"]["name"] == "sample-cli"
    assert config["build-system"]["build-backend"] == "uv_build"
    assert config["project"]["requires-python"] == ">=3.14"
    assert config["project"]["scripts"]["sample-cli"] == "sample_cli.cli:main"
    assert all(
        any(dependency.startswith(name) for dependency in config["project"]["dependencies"])
        for name in ("cyclopts", "loguru", "orjson", "platformdirs", "rich", "ruamel.yaml")
    )
    assert set(config["dependency-groups"]["dev"]) == {"pre-commit", "pytest", "pytest-testmon", "ruff"}
    assert (generated / "src" / "sample_cli" / "cli.py").is_file()
    assert not (generated / ".github" / "workflows" / "template-ci.yml").exists()
    config_source = generated / "src" / "sample_cli" / "config.py"
    assert config_source.is_file()
    assert 'APP_NAME = "sample-cli"' in config_source.read_text(encoding="utf-8")
    assert "class LoggingConfig:" in config_source.read_text(encoding="utf-8")
    assert (generated / "src" / "sample_cli" / "__main__.py").is_file()
    assert (generated / "src" / "sample_cli" / "errors.py").is_file()
    for module in ("database", "doctor", "output", "logging_utils"):
        assert (generated / "src" / "sample_cli" / f"{module}.py").is_file()
        assert (generated / "tests" / f"test_{module}.py").is_file()
    assert (generated / "tests" / "test_cli.py").is_file()
    assert (generated / "tests" / "test_config.py").is_file()
    assert (generated / ".python-version").read_text().strip() == "3.14.7"


def test_generated_workflow_calls_central_ci_only_on_pr(generated: Path) -> None:
    workflow = (generated / ".github" / "workflows" / "ci.yml").read_text()
    assert "pull_request:" in workflow
    assert "workflow_dispatch:" not in workflow
    assert "push:" not in workflow
    assert "schedule:" not in workflow
    assert "RuchirChawdhry/ci-workflows/.github/workflows/python-cli.yml@main" in workflow
    assert "RuchirChawdhry/ci-workflows/.github/workflows/python-build.yml@main" in workflow
    assert "cli-command: 'sample-cli'" in workflow
    assert "3.14.7" in workflow
    assert not (generated / ".github" / "workflows" / "ci.yml.jinja").exists()


def test_generated_project_has_agent_and_update_context(generated: Path) -> None:
    assert (generated / "AGENTS.md").is_file()
    assert (generated / ".copier-answers.yml").is_file()
    assert (generated / "config.example.yml").is_file()
    assert not (generated / "copier.yml").exists()


def test_generated_taskfile(generated: Path) -> None:
    taskfile = yaml.safe_load((generated / "Taskfile.yml").read_text(encoding="utf-8"))
    tasks = taskfile["tasks"]
    assert set(tasks) == {
        "setup",
        "dev",
        "test",
        "test:all",
        "lint",
        "fix",
        "build",
        "install",
        "clean",
        "doctor",
        "update",
    }
    assert tasks["setup"]["cmds"][0] == "uv sync --group dev"
    assert "uv run --no-sync pre-commit install" in tasks["setup"]["cmds"][1]
    assert "git rev-parse --show-prefix" in tasks["setup"]["cmds"][1]
    assert tasks["dev"]["cmds"] == [
        "uv run sample-cli {{if .CLI_ARGS}}{{.CLI_ARGS}}{{else}}--help{{end}}"
    ]
    assert tasks["test"]["cmds"][0] == "uv run pytest --testmon -q {{.CLI_ARGS}}"
    assert "--testmon-noselect" in tasks["test:all"]["cmds"][0]
    assert tasks["doctor"]["cmds"] == ["uv run sample-cli doctor {{.CLI_ARGS}}"]
    install = tasks["install"]["cmds"][0]
    assert "uv tool install --reinstall --python 3.14.7 ." in install
    assert "uv tool update-shell" in install
    assert "pipx ensurepath" in install


def test_generated_pre_commit_hooks(generated: Path) -> None:
    config = yaml.safe_load((generated / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
    assert len(config["repos"]) == 1
    repo = config["repos"][0]
    assert repo["repo"] == "local"
    hooks = repo["hooks"]
    assert [hook["id"] for hook in hooks] == ["ruff-check", "ruff-format"]
    assert [hook["entry"] for hook in hooks] == [
        "uv run --no-sync ruff check --fix --force-exclude",
        "uv run --no-sync ruff format --force-exclude",
    ]
    assert all(hook["types"] == ["python"] for hook in hooks)
