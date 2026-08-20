# AGENTS.md

## Project overview

This repository is `sshreader`, a Python library for parallel SSH operations built on Paramiko.

Key project files:
- `sshreader/` — package implementation
- `tests/` — unit tests
- `pyproject.toml` — project configuration and dependencies
- `Makefile` — common dev/test/lint commands

## Required working rules

### Python environment

Whenever working with Python modules, commands, tests, or tooling in this repository, always use the project-local virtual environment at `.venv`.

Use commands such as:
- `./.venv/bin/python`
- `./.venv/bin/pytest`
- `./.venv/bin/ruff`
- `./.venv/bin/ty`

Do not use bare `python`, `pytest`, `pip`, or `ruff` from the system environment when working on this repo. The local `.venv` is the source of truth for package resolution and project execution.

If the virtual environment is missing, create it before running Python work:

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install -e .
```

If the repo uses `uv` for project commands, prefer the local `.venv` for direct Python execution and module-level work; do not bypass the project environment with the system interpreter.

## Development expectations

- Keep changes consistent with the existing package layout and Python 3.10+ conventions.
- Prefer small, targeted edits.
- Run the relevant tests and lint checks before concluding work.
- For Python code, use the repository virtual environment rather than any global interpreter.

## Common verification commands

Use the local environment for project checks:

```bash
./.venv/bin/pytest
./.venv/bin/ruff check sshreader tests
./.venv/bin/ty check sshreader
```

## Notes

This file is intended to guide agents and contributors working in this repository so they use the same environment and coding conventions throughout the project.
