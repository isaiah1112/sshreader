.. faq documentation master file, created by Jesse Almanrode

FAQ
===

Why are my print statements funky?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Often times with multiprocessing print statements come out funky because multiple processes are writing to
:code:`sys.stdout` at the same time.  One of the ways you can deal with this is by implementing a
`multiprocessing.Lock()`_.  An example of how to use the lock in a pre or post hook is shown below:

.. code-block:: python

    from multiprocessing import Lock
    # Make the Lock object global so all child processes can use it
    _print_lock_ = Lock()

    def my_hook(*args):
        """ Process safe print for pre/post hook

        :param args: Tuple of ( *args, <ServerJob> )
        :return: None
        """
        global _print_lock_
        thisjob = list(args).pop()
        with _print_lock_:
            print(str(thisjob.name))
        return None

.. note::

    After :code:`sshreader v3.2` you can also use the new :code:`sshreader.echo` method to automatically implement a
    :code:`multiprocessing.Lock` on the fly.

Where did my output go?
~~~~~~~~~~~~~~~~~~~~~~~

Say you have a script (that uses sshreader or otherwise) that you are piping the output from to another unix command.
Something similar to the following:

.. code-block:: bash

    ./myscript.py | wc

but you keep getting 0 from the output of :code:`wc`. This is due to the `stdout buffer`_ in your terminal.
To overcome this "feature" either run your script as follows:

.. code-block:: bash

    python -u myscript.py | wc

or change the shebang at the top of your python script to:

.. code-block:: bash

    #!/usr/bin/env python -u

or by adding the following to your code directly after a print statement:

.. code-block:: python

    # Print something to stdout and immediately flush (unbuffered output)
    print('Unbuffered output')
    sys.stdout.flush()  # In Python 3.3 and above you can alternatively pass flush=True to the print statement

.. note::

    As of sshreader v3.4.4 the :code:`sshreader.echo` method issues a :code:`sys.stdout.flush()` after
    calling the standard Python print function, giving you easy access to unbuffered output.

Byte-String vs. Unicode-String
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In Python 2, strings are actually able to handle both byte-strings and unicode strings where in Python 3 all strings are
only unicode strings.  This can cause issues when working with both and using a module like sshreader (because output from
Paramiko and the subprocess module are byte-strings).  However, there is hope because sshreader includes a kwarg that can
enable automatic decoding of byte-strings to unicode strings.

.. code-block:: python

    import sshreader

    # sshreader can automatically decode bytestrings for you (for stdout and stderr)
    # This works for both the shell_command and ssh_command methods
    uname_cmd = sshreader.shell_command('uname -a', decodebytes=True)
    uname_cmd.stdout.split(',')

.. note::

    As of version 3.3 the default behavior for sshreader is to automatically decode byte strings to unicode strings.  If
    you would like it do NOT decode byte strings then use this flag, setting it to :code:`False`.

Pseduo Terminals
~~~~~~~~~~~~~~~~

Sometimes when using SSH you will see an error like the following:

.. code-block:: python

    import sshreader
    with sshreader.SSH('myhost.example.com', username='jdoe', keyfile='~/.ssh/id_rsa') as s:
        s.ssh_command('sudo touch /')
    >> ShellCommand(cmd='sudo touch /', stdout='', stderr='sudo: sorry, you must have a tty to run sudo', return_code=1)

This is due to not having a terminal definition in your SSH connection.  Normally the method for fixing this type of error
is to disable :code:`!requiretty` in your :code:`/etc/sudoers` file.  However, a quicker way to get around this is to request a
pseudo terminal when creating your ssh connection.  Sshreader will do this for you when you use the :code:`combine` option
when sending an :code:`ssh_command`.

.. note::

    When using a pseudo terminal stderr is piped to stdout.  At the moment this is simply just a "feature" of paramiko.
    If this ever changes in the future we will certainly support pseudo terminals with stdout and stderr as separate outputs.

Changing Logging
~~~~~~~~~~~~~~~~

As of :code:`sshreader v3.5` you might have noticed that the :code:`debuglevel` option is no longer available on :code:`ServerJob`
objects or the :code:`sshread` method.  To enable logging going forward you will want to change the level for the :code:`sshreader`
logger.

.. code-block:: python

    import logging
    logging.getLogger('sshreader').setLevel(logging.DEBUG)

To learn what levels can be set, check out the `logger module's documentation.`_


SSH Agent
~~~~~~~~~

With :code:`sshreader v4.1` (:code:`pydsh v2.4`) and later, I have ensured that Paramiko's support for utilizing keys held in
`SSH Agent`_ are available within the SSH class in sshreader.  To utilize them simply do not supply the SSH class with
either an SSH Keyfile or Password.  If there are keys cached in the agent, they will be used.  SSH Agent keys are also
now listed in the NamedTuple returned from the :code:`envvars()` method.

OpenSSH 8.8 and RSA SHA2
~~~~~~~~~~~~~~~~~~~~~~~~

In versions of OpenSSH 8.8 and later the default behavior is to not allow RSA keys with a SHA1 hash. While this is more secure, there are
times when you may still need to allow thes for connections to older servers.  :code:`sshreader v4.9.0` and later support an easy flag to
enable/disable this functionality within `Paramiko`_. By default, sshreader will allow the SHA1 keys unless you specifically enable the SHA2
support for RSA keys.

.. code-block:: python

    ssh  = sshreader.SSH('myhost.example.com', username='jdoe', keyfile='~/.ssh/id_rsa', connect=False)
    ssh.rsa_sha2 = True  # Enable new RSA security

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
.. _multiprocessing.Lock(): https://docs.python.org/2/library/multiprocessing.html#synchronization-between-processes
.. _stdout buffer: https://www.turnkeylinux.org/blog/unix-buffering
.. _logger module's documentation.: https://docs.python.org/3/library/logging.html#levels
.. _SSH Agent: https://en.wikipedia.org/wiki/Ssh-agent
.. _Paramiko: https://www.paramiko.org/changelog.html#2.9.0
