# Configuration

Settings are stored in the platform-specific user config directory, in config.yml. Use the application to discover the actual path.

```sh
uv run my-tool --config-path
uv run my-tool --init-config
uv run my-tool --show-config
uv run my-tool set-config logging.file_enabled false
uv run my-tool set-config cli.hello.name Ada
```

The root config flags are mutually exclusive. Use --path with --init-config, --show-config or set-config (not --config-path). The hello command accepts --config instead.

If the implicit config file is absent, reads use in-memory defaults. Initialization refuses to overwrite a file. set-config accepts dotted keys and YAML values, preserves unrelated settings and comments, and replaces the file via a sibling temporary file.

## Defaults and logging

```yaml
logging:
  file_level: INFO
  console_level: WARNING
  file_enabled: true
cli:
  hello:
    name: Ada
```

Explicit arguments override YAML command defaults, which override Python defaults. Cyclopts loads and validates these defaults for the sample hello command; other commands can opt in. Do not duplicate its argument merging.

Loguru uses independent named levels for file and console logs. --verbose selects DEBUG for the console, --quiet suppresses console logging, and neither changes file logging. Logs go to stderr or the platform-specific app.log; files rotate at 5 MB and are retained for 7 days. Help and configuration commands do not initialize logging.

Do not store secrets in YAML or log them. Prefer direct Loguru calls; optionally use @log_call for synchronous entry/duration/failure-type tracing or @logger.catch(reraise=True) for exceptions. Do not stack the two decorators.
