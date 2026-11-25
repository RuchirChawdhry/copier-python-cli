"""Exercise the installed wheel, never the source checkout."""

import json
import os
import subprocess


def run_cli(*args):
    result = subprocess.run(
        [os.environ["CLI_EXECUTABLE"], *args],
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def test_installed_configuration_and_greeting(tmp_path):
    config = tmp_path / "settings.yml"
    assert run_cli("--init-config", "--path", str(config), "--json") == {
        "path": str(config)
    }
    assert config.is_file()
    run_cli("set-config", "logging.file_enabled", "false", "--path", str(config))
    assert run_cli("--show-config", "--path", str(config), "--json")["logging"][
        "file_enabled"
    ] is False
    assert run_cli("hello", "--config", str(config), "--name", "Ada", "--json") == {
        "message": "Hello, Ada!"
    }
