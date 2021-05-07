.. pydsh documentation master file, created by Jesse Almanrode

pydsh
=====

Pydsh is a Python-based replication of `pdsh`_ that uses sshreader as the engine for parallelizing ssh tasks.  It
also attempts to format the output from commands for you in a easy to read manner.  Below are some examples of how it
can be used.

.. warning::

    With :code:`pydsh v1.3` I have moved away from the argparse module in favor of the `Click`_ module.  Some of the cli
    flags have changed.

Debugging
---------

In :code:`pydsh v2.6` I added better logging support for both the :code:`pydsh` script and the :code:`sshreader` module
which powers it.  There are 4 levels of debugging available to you:

* debug = pydsh:INFO
* debug + verbose = pydsh:INFO + sshreader:INFO
* debug + 2verbose = pydsh:DEBUG + sshreader:INFO
* debug + 3verbose = pydsh:DEBUG + sshreader:DEBUG

Keep in mind that most people will probably only ever need the INFO levels of debugging.  DEBUG levels may generate a lot
of output and are generally used to find issues within the script/module.

Examples
--------

Simplest form of pydsh [1]_.  Run a command and show the output of the commands as they complete: [2]_

.. code-block:: bash

    pydsh -w myhost[1-100].example.com 'uname -r'

.. note::

    When using the :code:`--dshbak` or :code:`--coalesce` options, a progress bar will be shown to the user as jobs
    are processing.

Run a script file rather than a simple command on remote hosts:

.. code-block:: bash

    pydsh -F -w myhost[1-100].example.com my_complex_script.sh

.. note::

    At this time scripts must have the first line start with :code:`#!` in order to be loaded and run as a script by pydsh.

Print output organized by host (similar to piping to :code:`dshbak` command):

.. code-block:: bash

    pydsh -D -w myhost[1-100].example.com 'uname -r'

Print output coalesced by host (similar to piping to :code:`dshbak -c` command):

.. code-block:: bash

    pydsh -C -w myhost[1-100].example.com 'uname -r'

Override ssh with a username/password combo:

.. code-block:: bash

    pydsh -u myuser -P Password1234 -w myhost[1-100].example.com 'uname -r'

Override ssh with a username/password combo (but prompt for the password):

.. code-block:: bash

    pydsh -u myuser -p -w myhost[1-100].example.com 'uname -r'

Run pydsh faster (uses multi-processing and multi-threading): [3]_

.. code-block:: bash

    pydsh --redline -w myhost[1-100].example.com 'uname -r'


Indices and tables
------------------

* :ref:`sshreader`
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
* `JA Computing`_

.. _JA Computing: http://www.jacomputing.net
.. _pdsh: https://github.com/chaos/pdsh
.. _hostlist expressions: https://www.nsc.liu.se/~kent/python-hostlist/
.. _Click: http://click.pocoo.org/6/
.. [1] Pydsh supports `hostlist expressions`_ to make listing hosts easier.
.. [2] Output can be piped to :code:`dshbak` command
.. [3] You may notice your fans spin up when using the :code:`redline` option. This is normal.
