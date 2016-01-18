.. pydsh documentation master file, created by Jesse Almanrode

pydsh
=====

Pydsh is a Python-based replication of `pdsh`_ that uses sshreader as the engine for parallelizing ssh tasks.  It
also attempts to format the output from commands for you in a easy to read manner.  Below are some examples of how it
can be used.

Examples
--------

Simplest form of pydsh [1]_.  Run a command, include a progress bar, and show the output of the commands:

.. code-block:: bash

    pydsh -w myhost[1-100].example.com 'uname -r'


Do not show a progress bar before the output and only show items with output:

.. code-block:: bash

    pydsh -u myuser -p mypass -w myhost[1-100].example.com -q 'uname -r'

Print output from jobs as soon as they complete (output can be piped to dshbak):

.. code-block:: bash

    pydsh -w myhost[1-100].example.com -Q 'uname -r' | dshbak -c

Finally, sort the output by commands that finished and commands that didn't:

.. code-block:: bash

    pydsh -u myuser -k ~/.ssh/id_dsa -w myhost[1-100].example.com -s 'uname -r'

.. [1] Pydsh supports `hostlist expressions`_ to make listing hosts easier.

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
