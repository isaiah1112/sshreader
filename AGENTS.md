# AGENTS.md

Project-wide development instructions for `sshreader`. Keep this file as the
single canonical source of repository guidance; `.github/copilot-instructions.md`
points here.

## Project

`sshreader` is a Python library built on Paramiko for parallel SSH operations.
The package implementation is in `sshreader/`, tests are in `tests/`, Sphinx
documentation is in `docs/`, and examples are in `examples/`.

Use `pyproject.toml` as the source of truth for package metadata, dependencies,
and Ruff configuration. The supported Python range is Python 3.11 and later
(currently tested on Python 3.11–3.15); keep the metadata, CI, and documentation
consistent when changing compatibility.

## Python environment

Use the project-local `.venv` for Python commands, tests, and tooling. Do not
run project Python commands with a system interpreter or install project
dependencies globally.

Use `uv` to create or synchronize the project environment and its dependencies:

```bash
uv sync --group test
uv sync --group test --group docs
```

For direct execution, use the explicit environment paths:

```bash
./.venv/bin/python
./.venv/bin/pytest
./.venv/bin/ruff
./.venv/bin/ty
```

If `.venv` is missing, `uv sync` can create it. Do not use `make install` for
environment setup; that Make target invokes the system `python`.

## Implementation conventions

- Keep changes focused and consistent with existing APIs and patterns. Preserve
  backward compatibility for Python 3.11 and later unless a requested change
  explicitly alters it.
- Follow the existing Python formatting and Ruff rules in `pyproject.toml`.
  Use modern annotations supported by Python 3.11, including `|` unions where
  appropriate.
- Keep imports ordered as in nearby modules: standard library, third-party,
  then package-local imports.
- Package modules use a module docstring followed by the LGPL copyright and
  license header. Match that layout when adding package modules.
- Document public APIs with docstrings. Follow nearby documentation conventions,
  including Sphinx/reStructuredText parameter, return, and exception fields
  where applicable.
- Reuse the project's structured types in `sshreader/customtypes.py` and
  preserve their public shapes when changing return values.
- Use context managers for SSH sessions and other resources where supported.
  Preserve secure SSH host-key verification defaults; do not silently weaken
  verification.
- Keep shell execution safe by default. If changing command execution behavior,
  preserve the existing distinction between shell-free execution and explicit
  shell use.
- Handle expected library errors explicitly. Avoid broad exception handling or
  silently converting failures into success-shaped results.
- Update directly related tests and documentation with behavior or API changes.

## Tests and checks

Tests use pytest and live in `tests/`. Run focused tests while iterating, then
the full suite when appropriate:

```bash
./.venv/bin/pytest
```

Run lint and type checks with the project tools:

```bash
./.venv/bin/ruff check sshreader tests
./.venv/bin/ty check sshreader
```

The Makefile also provides `make test`, `make lint`, `make coverage`, and
`make docs`; its `docker-test` target defaults to Python 3.15 and accepts an
override through `PYTHON_VERSION`.

For documentation changes, build the Sphinx site with the `docs` dependency
group, for example:

```bash
uv run --group docs sphinx-build -b html docs/source/ docs/build/html/
```

Do not edit `uv.lock` by hand. When changing project dependencies or Python
compatibility metadata, regenerate it with `uv lock` and verify it with
`uv lock --check`.
