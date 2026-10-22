pydsh
=====

:code:`pydsh` runs a command on multiple hosts using SSHreader. It expands hostlist expressions and can print results as jobs complete, group output by host, or coalesce identical output.

Installation
------------

The :code:`pydsh` executable is installed with the :code:`sshreader` package:

.. code-block:: bash

    python -m pip install sshreader

Examples
--------

Run a command on a host list:

.. code-block:: bash

    pydsh -w 'web[01-10].example.com' 'uname -r'

By default, :code:`pydsh` uses the current username and discovered SSH keys or the SSH agent. Supply a username and private key explicitly with :code:`-u` and :code:`-k`:

.. code-block:: bash

    pydsh -u jdoe -k ~/.ssh/id_ed25519 -w 'web[01-10].example.com' 'uname -r'

Use :code:`-p` to be prompted for a password, or :code:`-P` to provide one on the command line. Be aware that command-line passwords may be visible to other local users through process inspection or shell history.

Group command output by host with :code:`-D`, or coalesce identical output with :code:`-C`:

.. code-block:: bash

    pydsh -D -w 'web[01-10].example.com' 'uname -r'
    pydsh -C -w 'web[01-10].example.com' 'uname -r'

Run a script file on each host with :code:`-F`. The script must start with a shebang line (for example, :code:`#!/usr/bin/env bash`). By default, :code:`pydsh` asks for confirmation before executing the script; use :code:`--confirm` to skip that prompt:

.. code-block:: bash

    pydsh -F -w 'web[01-10].example.com' ./maintenance.sh

Options
-------

.. list-table::
   :header-rows: 1
   :widths: 24 76

   * - Option
     - Description
   * - :code:`-w`, :code:`--hostlist EXPR`
     - Required hostlist expression. Host entries may include an SSH port, such as :code:`host.example.com:2222`.
   * - :code:`-u`, :code:`--username`
     - SSH username; defaults to the current username when discoverable.
   * - :code:`-k`, :code:`--keyfile`
     - Private key file to use.
   * - :code:`-K`, :code:`--keypass`
     - Prompt for the private key passphrase.
   * - :code:`-p`, :code:`--prompt`
     - Prompt for the SSH password.
   * - :code:`-P`, :code:`--password`
     - Supply the SSH password on the command line.
   * - :code:`-D`, :code:`--dshbak`
     - Group output by host.
   * - :code:`-C`, :code:`--coalesce`
     - Coalesce similar output from hosts.
   * - :code:`-F`, :code:`--file`
     - Treat the command argument as a script file.
   * - :code:`--confirm`
     - Skip the script execution confirmation prompt.
   * - :code:`--redline`
     - Use multiprocessing and multithreading for job execution.
   * - :code:`--port`
     - Default SSH port (22).
   * - :code:`--timeout`
     - SSH command timeout in seconds (30 by default).
   * - :code:`-d`, :code:`--debug`
     - Enable debug output; :code:`-v` can be repeated to increase verbosity.
   * - :code:`--help`
     - Display all options and usage information.

When :code:`-D` or :code:`-C` is enabled, :code:`pydsh` buffers job output and displays a progress bar. Without output aggregation, results are printed as jobs complete. The :code:`--redline` option uses multiprocessing, so invoke :code:`pydsh` as a command-line program rather than calling its CLI from unguarded multiprocessing code.

Indices and tables
------------------

* :ref:`sshreader`
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
