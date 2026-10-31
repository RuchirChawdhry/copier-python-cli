"""Copier-template contract tests. Run: uv run --no-project --with copier --with pytest pytest tests."""

import tomllib
from pathlib import Path

import pytest
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
        unsafe=False,
    )
    return destination


def test_template_repo_workflows_are_inert() -> None:
    assert not (ROOT / ".github" / "workflows").exists()
    assert (ROOT / "template" / ".github" / "workflows" / "ci.yml.jinja").exists()


def test_generated_package_metadata(generated: Path) -> None:
    with (generated / "pyproject.toml").open("rb") as stream:
        config = tomllib.load(stream)
    assert config["project"]["name"] == "sample-cli"
    assert config["build-system"]["build-backend"] == "uv_build"
    assert config["project"]["requires-python"] == ">=3.14"
    assert config["project"]["scripts"]["sample-cli"] == "sample_cli.cli:app"
    assert all(
        any(dependency.startswith(name) for dependency in config["project"]["dependencies"])
        for name in ("cyclopts", "rich", "ruamel.yaml")
    )
    assert (generated / "src" / "sample_cli" / "cli.py").is_file()
    assert (generated / "src" / "sample_cli" / "config.py").is_file()
    assert (generated / "src" / "sample_cli" / "__main__.py").is_file()
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
