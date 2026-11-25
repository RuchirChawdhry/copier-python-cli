"""Read-only runtime and environment checks."""

import os
import platform
import sqlite3
import sys
from collections.abc import Iterator
from contextlib import closing
from pathlib import Path

from ruamel.yaml.error import YAMLError

from .config import LoggingConfig, default_config_path, default_log_path, read_settings
from .database import SCHEMA_VERSION, default_database_path

CHECK_COUNT = 7


def check(name: str, ok: bool, detail: str) -> dict[str, str | bool]:
    return {"name": name, "ok": ok, "detail": detail}


def check_path(name: str, path: Path) -> dict[str, str | bool]:
    """Find the nearest existing directory without creating anything."""
    parent = next((p for p in path.parents if p.exists()), path.parent)
    ok = parent.is_dir() and os.access(parent, os.W_OK | os.X_OK)
    if path.exists():
        ok = ok and path.is_file() and os.access(path, os.R_OK | os.W_OK)
    return check(name, ok, str(path))


def check_database(path: Path) -> dict[str, str | bool]:
    """Probe SQLite and inspect the on-disk schema without creating journal sidecars."""
    try:
        with closing(sqlite3.connect(":memory:")) as db:
            db.execute("SELECT 1").fetchone()
        if path.exists():
            uri = path.resolve().as_uri() + "?mode=ro&immutable=1"
            with closing(sqlite3.connect(uri, uri=True)) as db:
                version = db.execute("PRAGMA user_version").fetchone()[0]
                db.execute("SELECT key, value FROM records LIMIT 0")
            return check(
                "sqlite", version == SCHEMA_VERSION, f"{sqlite3.sqlite_version}; schema {version}"
            )
        return check("sqlite", True, f"{sqlite3.sqlite_version}; database not initialized")
    except sqlite3.Error as error:
        return check("sqlite", False, str(error))


def run_checks() -> Iterator[dict[str, str | bool]]:
    config = default_config_path()
    database = default_database_path()
    yield check("python", sys.version_info >= (3, 14), platform.python_version())
    yield check("platform", True, platform.system() + " " + platform.machine())
    try:
        LoggingConfig.from_config(read_settings())
        detail = "valid YAML" if config.exists() else "using defaults"
        yield check("config", True, f"{config}: {detail}")
    except (OSError, ValueError, TypeError, YAMLError) as error:
        yield check("config", False, f"{config}: {error}")
    yield check_path("config_path", config)
    yield check_path("logs", default_log_path())
    yield check_path("database_path", database)
    yield check_database(database)
