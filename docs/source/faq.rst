.. faq documentation master file, created by Jesse Almanrode

FAQ
===

Find answers to the frequently answered questions here.

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

Of course, you can also do as the link above says and force :code:`sys.stdout.flush()` but I am not a fan of that
particular method.

Byte-String vs. Unicode-String
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In Python 2, strings are actually able to handle both byte-strings and unicode strings and in Python 3 all strings are
now unicode-strings.  This can cause issues when working with both and using a module like sshreader (because output from
Paramiko and the subprocess module are byte-strings).  However, there are a few things you can do to make this far easier.

Ensure all literal strings are unicode and convert all byte strings to unicode!

.. code-block:: python

    from __future__ import unicode_literals
    import sshreader

    # sshreader can automatically decode bytestrings for you (for stdout and stderr)
    # This works for both the shell_command and ssh_command methods
    uname_cmd = sshreader.shell_command('uname -a', decodebytes=True)
    uname_cmd.stdout.split(',')

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
