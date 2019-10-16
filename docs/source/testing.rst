.. testing documentation master file, created by Jesse Almanrode

Testing
===============

Locally Using Tox
-----------------

If you would like to test locally using :code:`tox`, simply add a :code:`test_params.json` to the :code:`tests` directory
with the following parameters:

.. code-block:: json

    {"host_fqdn": "127.0.0.1",
      "ssh_user": "jdoe",
      "ssh_password": "password1234",
      "ssh_key_path": "~/.ssh/id_rsa"
    }

Then, simply specify the python version you would like to test with:

.. code-block:: bash

    tox -e py38  # Test Python3.8
    tox -e py37  # Test Python3.7
    tox -e py36  # Test Python3.6
    tox -e py35  # Test Python3.5
    tox -e py34  # Test Python3.4
    tox -e py27  # Test Python2.7

Or to test all the above versions:

.. code-block:: bash

    tox  # Will test py27, py34, py35, py36, py37, py38

Bitbucket Pipelines
-------------------

SSHreader uses Docker within `Bitbucket Pipelines`_ to run the automated tests across the various versions of Python.  If you
would like to use docker image used by :code:`sshreader` to run the openssh for local testing simply do the following:

.. code-block:: bash

    docker run -rm --publish=22 isaiah1112/sshreader:latest

Then you should be able to simply run:

.. code-block:: bash

    tox

Indices and tables
------------------

* :ref:`sshreader`
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
* `JA Computing`_

.. _JA Computing: http://www.jacomputing.net
.. _Bitbucket Pipelines: https://bitbucket.org/isaiah1112/sshreader/addon/pipelines/home#!/
