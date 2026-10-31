"""Read YAML configuration without coupling it to the CLI/UI."""

from pathlib import Path
from typing import Any

from ruamel.yaml import YAML


def load_config(path: Path) -> dict[str, Any]:
    """Return a YAML mapping, rejecting empty or non-mapping documents."""
    yaml = YAML(typ="safe")
    with path.open(encoding="utf-8") as stream:
        data = yaml.load(stream)
    if not isinstance(data, dict):
        raise ValueError("Configuration must be a YAML mapping")
    return data
