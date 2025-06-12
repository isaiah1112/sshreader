Local Testing
=============

In order to make the testing/integration process as simple as possible, I utilize a custom `Docker Image`_ to run an ssh
server.  To begin configuring your system for local testing, please `install Docker`_ first. After you have installed
Docker and have it running, simply run the following command:

.. code-block:: bash

    make test

This command pulls down the custom docker image, runs it on port :code:`22`, and then runs all the unit/integration
tests.  If you would like to change which port this container runs on, simply export the :code:`SSH_PORT=<int>` environment
variable prior to running :code:`make test` to whatever integer port you would like to map this container to.

To clean up after running the tests (stopping external docker containers) run:

.. code-block:: bash

    make test-clean

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
.. _Docker Image: https://hub.docker.com/repository/docker/isaiah1112/sshreader
.. _install Docker: https://www.docker.com/get-started/
.. _Bitbucket Pipelines: https://bitbucket.org/isaiah1112/sshreader/addon/pipelines/home#!/
