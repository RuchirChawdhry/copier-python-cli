"""Exercise the installed wheel outside the generated source tree."""

import json
import os
import sqlite3
import subprocess
from pathlib import Path

import pytest


@pytest.fixture
def run_cli(tmp_path, monkeypatch):
    for name, directory in (
        ("HOME", "home"),
        ("XDG_CONFIG_HOME", "config"),
        ("XDG_DATA_HOME", "data"),
        ("XDG_STATE_HOME", "state"),
        ("XDG_CACHE_HOME", "cache"),
    ):
        path = tmp_path / directory
        path.mkdir()
        monkeypatch.setenv(name, str(path))
    monkeypatch.setenv("FORCE_COLOR", "1")
    executable = os.environ["CLI_EXECUTABLE"]

    def run(*args, check=True):
        result = subprocess.run(
            [executable, *args],
            cwd=tmp_path,
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )
        if check:
            assert result.returncode == 0, (
                f"{result.args!r} exited {result.returncode}\n"
                f"stdout: {result.stdout}\nstderr: {result.stderr}"
            )
        return result

    return run


def test_installed_machine_output(run_cli):
    result = run_cli("hello", "--name", "Agent", "--json", "--verbose")
    assert json.loads(result.stdout) == {"message": "Hello, Agent!"}
    assert "Greeting requested" in result.stderr
    assert "\x1b" not in result.stdout + result.stderr

    result = run_cli("hello", "--jsonl", "--quiet")
    assert len(result.stdout.splitlines()) == 1
    assert json.loads(result.stdout) == {"message": "Hello, world!"}
    assert result.stderr == ""


def test_installed_configuration(run_cli, tmp_path):
    path = Path(json.loads(run_cli("--config-path", "--json").stdout)["path"])
    assert path.is_relative_to(tmp_path / "config")
    assert not path.exists()
    assert json.loads(run_cli("--init-config", "--json").stdout) == {"path": str(path)}
    original = path.read_bytes()
    result = run_cli("--init-config", "--json", check=False)
    assert result.returncode != 0
    assert result.stdout == ""
    assert path.read_bytes() == original

    run_cli("set-config", "logging.file_enabled", "false", "--json")
    run_cli("set-config", "logging.console_level", "INFO", "--json")
    run_cli("set-config", "cli.hello.name", "Ada", "--json")
    settings = json.loads(run_cli("--show-config", "--json").stdout)
    assert settings["logging"] == {
        "file_level": "INFO",
        "console_level": "INFO",
        "file_enabled": False,
    }
    assert settings["cli"]["hello"]["name"] == "Ada"
    result = run_cli("hello", "--json")
    assert json.loads(result.stdout) == {"message": "Hello, Ada!"}
    assert "Greeting requested" in result.stderr
    assert json.loads(run_cli("hello", "--name", "Grace", "--json").stdout) == {
        "message": "Hello, Grace!"
    }

    path.write_text("logging: [invalid-value\n", encoding="utf-8")
    result = run_cli("--show-config", "--json", check=False)
    assert result.returncode != 0
    assert result.stdout == ""
    assert "line 1" in result.stderr
    assert "column" in result.stderr


def test_installed_database_and_doctor(run_cli, tmp_path):
    path = Path(json.loads(run_cli("db-path", "--json").stdout)["path"])
    assert path.is_relative_to(tmp_path / "data")
    assert not path.exists()
    checks = json.loads(run_cli("doctor", "--json").stdout)
    assert checks and all(check["ok"] for check in checks)
    assert not path.exists()

    result = run_cli("db-list", "--json", "--jsonl", check=False)
    assert result.returncode != 0
    assert not path.exists()
    assert json.loads(run_cli("db-list", "--json").stdout) == []
    with sqlite3.connect(path) as db:
        assert db.execute("PRAGMA journal_mode").fetchone()[0] == "wal"
        db.execute("INSERT INTO records (key, value) VALUES (?, ?)", ("example", "value"))
    assert json.loads(run_cli("db-list", "--jsonl").stdout) == {
        "key": "example",
        "value": "value",
    }
