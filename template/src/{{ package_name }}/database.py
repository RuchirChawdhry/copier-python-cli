"""Local SQLite persistence. Keep application data separate from YAML settings."""

import sqlite3
from collections.abc import Iterator
from contextlib import closing, contextmanager
from pathlib import Path

from platformdirs import user_data_path

from .config import APP_NAME
from .errors import ApplicationError

SCHEMA_VERSION = 1


def default_database_path() -> Path:
    return user_data_path(APP_NAME, appauthor=False) / "data.sqlite3"


@contextmanager
def connect(path: Path | None = None) -> Iterator[sqlite3.Connection]:
    """Open a transaction; commit on success, roll back on error, always close."""
    path = default_database_path() if path is None else path
    path.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(path, timeout=5, autocommit=True)) as db:
        db.row_factory = sqlite3.Row
        mode = db.execute("PRAGMA journal_mode = WAL").fetchone()[0]
        if mode.lower() != "wal":
            raise sqlite3.OperationalError(f"Could not enable WAL: {mode}")
        db.execute("PRAGMA foreign_keys = ON")
        db.autocommit = False
        with db:
            version = db.execute("PRAGMA user_version").fetchone()[0]
            match version:
                case 0:
                    db.execute(
                        "CREATE TABLE IF NOT EXISTS records "
                        "(key TEXT PRIMARY KEY, value TEXT NOT NULL)"
                    )
                    db.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")
                case 1:
                    pass
                case _:
                    raise ApplicationError(f"Unsupported database schema version: {version}")
            yield db


def set_record(key: str, value: str, path: Path | None = None) -> dict[str, str]:
    with connect(path) as db:
        db.execute(
            "INSERT INTO records (key, value) VALUES (?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (key, value),
        )
    return {"key": key, "value": value}


def get_record(key: str, path: Path | None = None) -> dict[str, str] | None:
    with connect(path) as db:
        row = db.execute("SELECT key, value FROM records WHERE key = ?", (key,)).fetchone()
    return dict(row) if row is not None else None


def list_records(path: Path | None = None) -> list[dict[str, str]]:
    with connect(path) as db:
        return [dict(row) for row in db.execute("SELECT key, value FROM records ORDER BY key")]
