UV_PATH := $(shell which uv 2>/dev/null)

.PHONY: help
help:
	@echo "Usage: make <target>"
	@echo "\nTargets:"
	@echo "  install               Install this package (pip install)"
	@echo "  docs                  Build Sphinx documentation"
	@echo "  test                  Run unit tests"
	@echo "  coverage              Build an HTML coverage report"
	@echo "  lint                  Run 'ruff' linting and 'ty' type-checking on project"

# Install UV if not installed
.PHONY: uv-init
uv-init:
	@if [ -z "$(UV_PATH)" ]; then curl -LsSf https://astral.sh/uv/install.sh | sh; fi

.PHONY: install
install:
	@python -m pip install .

.PHONY: docs
docs: uv-init
	@uv run --group docs sphinx-build -b html docs/source/ docs/build/html/

.PHONY: test
test:
	@uv run --group test coverage run -m pytest

.PHONY: coverage
coverage: test
	@uv run --group test coverage html

.PHONY: lint
lint: uv-init
	@uv run --group test ruff check sshreader/
	@uv run --group test ty check sshreader/
