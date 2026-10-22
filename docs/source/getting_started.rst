Getting Started
===============

Installation
------------

Install SSHreader from PyPI:

.. code-block:: bash

    python -m pip install sshreader

SSHreader supports Python 3.11 and later.

Connecting to one host
----------------------

Use :class:`sshreader.ssh.SSH` to open a connection and run commands. A context manager closes the connection when the block ends. Authentication can use a private key, an SSH agent, or a password.

.. code-block:: python

    from sshreader import SSH

    with SSH("myhost.example.com", username="jdoe", keyfile="~/.ssh/id_ed25519") as ssh:
        result = ssh.ssh_command("uname -a")
        print(result.stdout)
        print(result.return_code)

SSHreader loads system host keys and uses Paramiko's warning policy for hosts without a known key. Unknown host keys are accepted after a warning, so ensure the host is present in a trusted known-hosts file when host identity must be verified. You can provide an additional known-hosts file with :code:`known_hosts`. Set :code:`allow_unknown_hosts=True` only when you intentionally want unknown host keys to be accepted automatically.

Running jobs on multiple hosts
------------------------------

:class:`sshreader.utils.ServerJob` represents one host and one or more commands. Commands in a job run sequentially. Pass a list of jobs to :func:`sshreader.utils.sshread` to run them concurrently:

.. code-block:: python

    from sshreader import ServerJob, sshread

    hosts = ["server1.example.com", "server2.example.com"]
    jobs = [
        ServerJob(
            host,
            ["hostname", "uptime"],
            username="jdoe",
            keyfile="~/.ssh/id_ed25519",
        )
        for host in hosts
    ]

    finished_jobs = sshread(jobs, tcount=0)
    for job in finished_jobs:
        print(job.name, job.status)
        for result in job.results:
            print(result.cmd, result.stdout, result.stderr, result.return_code)

Each result provides :code:`cmd`, :code:`stdout`, :code:`stderr`, and :code:`return_code`. A job's :code:`results` list contains its command results, and :code:`status` is the sum of the command return codes (or 255 if the SSH connection failed). Jobs are returned in completion order, not necessarily in the order they were submitted.

Set :code:`tcount=0` to let SSHreader choose a thread count based on the CPU limit and number of jobs. Set :code:`pcount=0` to use processes; you may combine processes and threads with :code:`pcount` and :code:`tcount`. With multiprocessing, use the standard entry-point guard:

.. code-block:: python

    if __name__ == "__main__":
        finished_jobs = sshread(jobs, pcount=0, tcount=0)

The :func:`sshreader.utils.sshread` function takes a list, including when running one job: :code:`sshread([job], tcount=0)`.

Hooks
-----

Use :class:`sshreader.utils.Hook` to call a function before or after a job. The job is passed to the hook. By default, a pre-hook runs before connecting and a post-hook runs after disconnecting. Set :code:`ssh_established=True` to run the hook while the job's SSH connection is open.

.. code-block:: python

    from sshreader import Hook, ServerJob, sshread

    def report_host(job):
        print(job.name)

    job = ServerJob(
        "myhost.example.com",
        "hostname",
        username="jdoe",
        keyfile="~/.ssh/id_ed25519",
        pre_hook=Hook(target=report_host),
    )

    if __name__ == "__main__":
        sshread([job], tcount=1)

Local commands
--------------

Use :func:`sshreader.utils.shell_command` to run a command locally, or set :code:`run_local=True` on a :class:`sshreader.utils.ServerJob` to run local jobs through :func:`sshreader.utils.sshread`.

.. code-block:: python

    from sshreader import shell_command

    result = shell_command("uname -a")
    print(result.stdout)

Local string commands are split into arguments and run without a shell by default. To intentionally run through the shell, pass :code:`shell=True`; do not use this with untrusted command input.

SSH helpers and SFTP
--------------------

The :func:`sshreader.ssh.envvars` helper returns an :class:`sshreader.customtypes.EnvVars` tuple containing the username, discovered private-key paths, and keys available through the SSH agent.

Use :meth:`sshreader.ssh.SSH.sftp_put` and :meth:`sshreader.ssh.SSH.sftp_get` to transfer files over an established SSH connection:

.. code-block:: python

    from sshreader import SSH

    with SSH("myhost.example.com", username="jdoe", keyfile="~/.ssh/id_ed25519") as ssh:
        ssh.sftp_put("./report.txt", "/tmp/report.txt")
        ssh.sftp_get("/tmp/result.txt", "./result.txt")

See :doc:`sshreader` and :doc:`ssh` for the complete API reference and :doc:`pydsh` for the command-line tool.

Indices and tables
------------------

* :ref:`sshreader`
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
