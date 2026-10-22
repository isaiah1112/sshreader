Local Testing
=============

The project uses :code:`uv` to manage its development environment. From the repository root, install the test dependencies and run the test suite with:

.. code-block:: bash

    uv sync --group test
    uv run --group test pytest


You can also use the Makefile targets :code:`make test`, :code:`make lint`, and :code:`make coverage`.

Run :code:`ruff` and :code:`ty` checks with:

.. code-block:: bash

    uv run --group test ruff check sshreader tests
    uv run --group test ty check sshreader

Testing Coverage
----------------

To generate an HTML coverage report, run:

.. code-block:: bash

    make coverage

Open :code:`htmlcov/index.html` in a browser to view the report.

To test against a specific Python version in Docker, use :code:`make docker-test PYTHON_VERSION=3.15` (the default is Python 3.15).

Indices and tables
------------------

* :ref:`sshreader`
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
* `JA Computing`_

.. _JA Computing: http://www.jacomputing.net
