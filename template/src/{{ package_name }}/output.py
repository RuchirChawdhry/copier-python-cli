"""One output contract for human users and automation."""

import sys
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from typing import Annotated, Any

import orjson
from cyclopts import Group, Parameter, validators
from rich.console import Console
from rich.progress import Progress

from .errors import ApplicationError

FORMAT_GROUP = Group("Output format", validator=validators.MutuallyExclusive())
VERBOSITY_GROUP = Group("Output verbosity", validator=validators.MutuallyExclusive())


@Parameter(name="*", negative=())
@dataclass(frozen=True)
class OutputOptions:
    json: Annotated[bool, Parameter(group=FORMAT_GROUP)] = False
    """Emit one JSON document."""
    jsonl: Annotated[bool, Parameter(group=FORMAT_GROUP)] = False
    """Emit one JSON record per line."""
    quiet: Annotated[bool, Parameter(group=VERBOSITY_GROUP)] = False
    """Suppress progress and diagnostic logs; retain results and errors."""
    verbose: Annotated[bool, Parameter(group=VERBOSITY_GROUP)] = False
    """Enable debug diagnostics on stderr."""


class Output:
    def __init__(self, options: OutputOptions | None = None) -> None:
        self.options = options or OutputOptions()
        console_options = {"force_terminal": False, "color_system": None} if self.machine else {}
        self.stdout = Console(**console_options)
        self.stderr = Console(stderr=True, **console_options)

    @property
    def machine(self) -> bool:
        return self.options.json or self.options.jsonl

    def emit(self, data: Any, *, human: Any = None) -> None:
        """Results only on stdout; machine output never passes through Rich."""
        if self.options.json:
            self.write_json(data)
        elif self.options.jsonl:
            records = data if isinstance(data, list) else [data]
            for record in records:
                self.write_json(record)
        elif isinstance(human, str):
            self.stdout.print(human, markup=False, highlight=False, soft_wrap=True)
        else:
            self.stdout.print(data if human is None else human)

    @staticmethod
    def write_json(data: Any) -> None:
        """Write compact UTF-8 JSON directly, with exactly one trailing newline."""
        try:
            payload = orjson.dumps(
                data, default=str, option=orjson.OPT_APPEND_NEWLINE | orjson.OPT_NON_STR_KEYS
            )
        except orjson.JSONEncodeError as error:
            raise ApplicationError(f"Could not serialize JSON: {error}") from error
        sys.stdout.buffer.write(payload)
        sys.stdout.buffer.flush()

    def note(self, message: str) -> None:
        """Verbose-only diagnostic; never contaminates stdout."""
        if self.options.verbose and not self.options.quiet:
            self.stderr.print(message, markup=False, highlight=False)

    def progress(self) -> Progress:
        """Rich progress for interactive humans, never for agent output or quiet mode."""
        return Progress(
            console=self.stderr,
            disable=self.machine or self.options.quiet or not self.stderr.is_terminal,
            transient=True,
        )

    def track[T](
        self, items: Iterable[T], *, description: str = "Working", total: int | None = None
    ) -> Iterator[T]:
        with self.progress() as progress:
            yield from progress.track(items, description=description, total=total)
