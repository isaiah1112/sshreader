Local Testing
=============

To run all unit tests in your current version of Python simply run:

.. code-block:: bash

    make test


To test :code:`ruff` linting and :code:`ty` typing, simply run:

.. code-block:: bash

    make lint

Testing Coverage
----------------

To generate a test coverage report, ensure all the requirements for running the unit/integration tests are installed and
running and then simply run the following command:

.. code-block:: bash

    make coverage

Then, open the HTML files in your default browser using :code:`open htmlcov/index.html`!

Indices and tables
------------------

* :ref:`sshreader`
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
* `JA Computing`_

.. _JA Computing: http://www.jacomputing.net
