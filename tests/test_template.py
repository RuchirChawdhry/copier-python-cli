"""End-to-end Copier template smoke tests (run on template PRs)."""

import subprocess
import tomllib
from pathlib import Path

import pytest
from copier import run_copy

TEMPLATE_ROOT = Path(__file__).resolve().parents[1]


def command(project: Path, *args: str) -> str:
    result = subprocess.run(
        args,
        cwd=project,
        capture_output=True,
        text=True,
        check=False,
        timeout=180,
    )
    assert result.returncode == 0, f"{' '.join(args)}\n{result.stdout}\n{result.stderr}"
    return result.stdout


@pytest.fixture
def sample_project(tmp_path: Path) -> Path:
    target = tmp_path / "sample-tool"
    run_copy(
        str(TEMPLATE_ROOT),
        target,
        defaults=True,
        data={
            "project_name": "sample-tool",
            "description": "A CLI for testing template generation.",
            "author_name": "Example Author",
            "python_version": "3.13",
        },
    )
    return target


def test_template_generates_project_metadata_and_layout(sample_project: Path) -> None:
    metadata = tomllib.loads((sample_project / "pyproject.toml").read_text())
    assert metadata["project"]["name"] == "sample-tool"
    assert metadata["project"]["scripts"]["sample-tool"] == "sample_tool.cli:app"
    assert metadata["build-system"]["build-backend"] == "uv_build"
    assert (sample_project / "src/sample_tool/cli.py").is_file()
    assert (sample_project / "tests/test_cli.py").is_file()
    assert (sample_project / ".copier-answers.yml").is_file()
    assert (sample_project / "AGENTS.md").is_file()
    assert (sample_project / ".github/workflows/ci.yml").is_file()
    assert "Example Author" in (sample_project / "LICENSE").read_text()
    assert not (sample_project / "copier.yml").exists()
    assert not (sample_project / "tests/test_template.py").exists()


def test_generated_cli_passes_quality_checks(sample_project: Path) -> None:
    command(sample_project, "uv", "sync", "--group", "dev")
    command(sample_project, "uv", "run", "--no-sync", "ruff", "check", ".")
    command(sample_project, "uv", "run", "--no-sync", "ruff", "format", "--check", ".")
    command(sample_project, "uv", "run", "--no-sync", "pytest", "-q")
    command(sample_project, "uv", "run", "--no-sync", "sample-tool", "--help")
    command(sample_project, "uv", "build")


def test_other_slug_keeps_module_and_entrypoint_consistent(tmp_path: Path) -> None:
    target = tmp_path / "another-cli"
    run_copy(str(TEMPLATE_ROOT), target, defaults=True, data={"project_name": "another-cli"})
    metadata = tomllib.loads((target / "pyproject.toml").read_text())
    assert metadata["project"]["scripts"]["another-cli"] == "another_cli.cli:app"
    assert (target / "src/another_cli/__main__.py").is_file()
