FAQ
===

How do I run a single job?
~~~~~~~~~~~~~~~~~~~~~~~~~~

:func:`sshreader.utils.sshread` takes a list of :class:`sshreader.utils.ServerJob` objects. Wrap one job in a list:

.. code-block:: python

    from sshreader import ServerJob, sshread

    job = ServerJob("myhost.example.com", "hostname", username="jdoe", keyfile="~/.ssh/id_ed25519")
    finished = sshread([job], tcount=1)

Why do results appear in a different order?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Jobs are returned as workers finish, so the list returned by :func:`sshreader.utils.sshread` is in completion order rather than input order. Use :code:`job.name` to associate each result with its host.

Why are concurrent print statements interleaved?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Multiple workers may write to standard output at the same time. If a hook or job prints output, pass :code:`print_lock=True` to :func:`sshreader.utils.sshread` and use :func:`sshreader.utils.echo` to serialize and flush output:

.. code-block:: python

    from sshreader import Hook, ServerJob, echo, sshread

    def print_host(job):
        echo(job.name)

    job = ServerJob(
        "myhost.example.com",
        "hostname",
        username="jdoe",
        keyfile="~/.ssh/id_ed25519",
        pre_hook=Hook(target=print_host),
    )

    sshread([job], tcount=1, print_lock=True)

Do I need a main guard for multiprocessing?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Yes. SSHreader uses Python's spawn process model. Protect the call that starts multiprocessing so child processes do not rerun the parent program:

.. code-block:: python

    if __name__ == "__main__":
        sshread(jobs, pcount=0, tcount=0)

Why is local shell syntax not interpreted?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:func:`sshreader.utils.shell_command` is shell-free by default. A string command is split into arguments, so shell operators such as :code:`&&`, pipes, and redirection are not interpreted by a shell. To intentionally use shell syntax, pass :code:`shell=True` and ensure command input is trusted:

.. code-block:: python

    from sshreader import shell_command

    result = shell_command("echo hello && uname -a", shell=True)

SSH commands run on the remote host through SSH and use the remote shell behavior provided by the SSH server.

How do I keep command output as bytes?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Output is decoded to strings by default. Pass :code:`decode_bytes=False` to :func:`sshreader.utils.shell_command`, or :code:`decodebytes=False` to :meth:`sshreader.ssh.SSH.ssh_command`, to preserve bytes.

What does :code:`combine=True` do?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For :meth:`sshreader.ssh.SSH.ssh_command`, :code:`combine=True` requests a pseudo-terminal and combines standard error with standard output. The result's :code:`stderr` is :code:`None`. For :func:`sshreader.utils.shell_command`, :code:`combine=True` redirects standard error to standard output without requesting a pseudo-terminal.

How are SSH host keys handled?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:class:`sshreader.ssh.SSH` loads system host keys and uses Paramiko's warning policy by default. Unknown host keys are accepted after a warning, so ensure the host is present in a trusted known-hosts file when host identity must be verified. You can load an additional known-hosts file with :code:`known_hosts`. The :code:`allow_unknown_hosts=True` option automatically accepts unknown keys and should only be used when that behavior is intentional.

How can I enable logging?
~~~~~~~~~~~~~~~~~~~~~~~~~

Set the :code:`sshreader` logger level using Python's :mod:`logging` module:

.. code-block:: python

    import logging

    logging.getLogger("sshreader").setLevel(logging.DEBUG)

See the :doc:`pydsh` page for command-line logging options.

Indices and tables
------------------

* :ref:`sshreader`
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
