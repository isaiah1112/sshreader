# Copilot Instructions for sshreader

## Project Overview

**sshreader** is a Python library that provides a multi-threaded/multi-process wrapper around Paramiko for parallel SSH operations across multiple servers. It is production-stable (v6.3.0) and supports Python 3.10+.

- **License:** GNU Lesser General Public License v3.0 or later
- **Key Dependencies:** paramiko, click, colorama, progressbar2, python-hostlist
- **Main Tools:** Ruff (linting), pytest (testing), Sphinx (docs)

## Code Style Guidelines

### Module Structure
- Every Python file starts with a module-level docstring
- Followed by the LGPL copyright header (2015-2026 Jesse Almanrode)
- Then imports organized by: stdlib → third-party → local modules

### Type Hints
- Use modern Python type hints (Python 3.10+ union syntax with `|`)
- NamedTuples for structured returns (Command, EnvVars, etc.)
- Type hints in function signatures with return type annotations
- Use `Optional[Type]` when values can be None

### Naming Conventions
- **Classes:** PascalCase (e.g., `SSH`, `EnvVars`, `Command`)
- **Functions/Methods:** snake_case (e.g., `shell_command()`, `envvars()`)
- **Constants:** UPPER_SNAKE_CASE
- **Private Methods:** prefix with `_` (e.g., `_connection`)

### Documentation
- All public classes and functions have docstrings
- Docstrings include parameter types, descriptions, and return types
- Use `:type`, `:param`, `:return`, `:rtype:` format in docstrings
- Exception documentation with `:raises:`

### Imports
```python
import logging
import os
from typing import Optional
import paramiko
from .customtypes import Command
```

### Logging
- Use `logging.getLogger(__name__)` with module-level logger
- Log level typically set to WARNING
- Disable propagation to root logger: `log.propagate = False`

### Context Managers
- Use `with` statements for SSH connections and resource management
- SSH class supports `__enter__` and `__exit__` for context manager protocol

## Linting Configuration

Ruff rules enabled: `E`, `F`, `B`, `UP`, `B`, `SIM`, `I`
Ignoring: `E501` (line length), `F401` (unused imports)

When submitting code, ensure it passes Ruff linting.

## Testing

- **Framework:** unittest
- **Test Location:** `tests/` directory
- **Naming:** `test_*.py` files with `Test*` classes
- **Test Methods:** Start with `test_`, include descriptive docstrings
- **Run Tests:** `make test` or direct pytest/unittest

### Test Patterns
```python
class TestSSH(unittest.TestCase):
    """Test cases for the SSH class"""
    
    def test_connection_with_password(self):
        """Test SSH connection using password authentication"""
        with sshreader.SSH(host, username=user, password=pwd) as conn:
            self.assertTrue(conn.alive())
```

## Project Layout

- `sshreader/` - Main package
  - `ssh.py` - SSH session wrapper around Paramiko
  - `utils.py` - Utility functions (shell_command, parallelization helpers)
  - `customtypes.py` - Type definitions (NamedTuples)
  - `scripts/pydsh.py` - CLI tool similar to pdsh
- `tests/` - Unit and integration tests
- `docs/` - Sphinx documentation
- `examples/` - Example scripts

## Build & Development

- **Package Manager:** PDM with uv backend
- **Install:** `pip install sshreader` or `make install`
- **Makefile:** Available for common tasks
- **Documentation:** Sphinx-based at https://sshreader.readthedocs.io/

## Key Principles

1. **Backwards Compatibility:** Maintain Python 3.10+ support
2. **Robust Error Handling:** Paramiko exceptions should be caught and handled appropriately
3. **Parallel Processing:** Leverage threading/multiprocessing for concurrent operations
4. **Clean Interfaces:** Simple, intuitive APIs for SSH operations
5. **Comprehensive Docs:** Docstrings and Sphinx documentation for all public APIs
