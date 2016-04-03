.. pydsh documentation master file, created by Jesse Almanrode

pydsh
=====

Pydsh is a Python-based replication of `pdsh`_ that uses sshreader as the engine for parallelizing ssh tasks.  It
also attempts to format the output from commands for you in a easy to read manner.  Below are some examples of how it
can be used.

.. note::

    With version 1.3 of pydsh I have moved away from uisng argparse in favor of the `Click`_ module.  Some of the cli
    flags might have changed.

Examples
--------

Simplest form of pydsh [1]_.  Run a command, include a progress bar, and show the output of the commands by host:

.. code-block:: bash

    pydsh -w myhost[1-100].example.com 'uname -r'

Do not show a progress bar before the output:

.. code-block:: bash

    pydsh -q -w myhost[1-100].example.com -q 'uname -r'

Print output from jobs as soon as they complete (output can be piped to dshbak):

.. code-block:: bash

    pydsh -D -w myhost[1-100].example.com 'uname -r' | dshbak -c

Override ssh with a username/password combo:

.. code-block:: bash

    pydsh -u myuser -P Password1234 -w myhost[1-100].example.com 'uname -r'

Override ssh with a username/password combo (but prompt for the password):

.. code-block:: bash

    pydsh -u myuser -p -w myhost[1-100].example.com 'uname -r'


Indices and tables
------------------

* :ref:`sshreader`
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
* `JA Computing`_

.. _JA Computing: http://www.jacomputing.net
.. _pdsh: https://computing.llnl.gov/linux/pdsh.html
.. _hostlist expressions: https://www.nsc.liu.se/~kent/python-hostlist/
.. _Click: http://click.pocoo.org/6/
.. [1] Pydsh supports `hostlist expressions`_ to make listing hosts easier.