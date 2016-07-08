.. faq documentation master file, created by Jesse Almanrode

Getting Started
===============

Installing sshreader
--------------------

The easiest way to get working with sshreader is to use :code:`pip` to install the module.  You can do that by running
the following in your terminal

.. code-block:: bash

    pip install sshreader

.. note::

    If you already have sshreader installed and would like to update to the latest release, run the following:

.. code-block:: bash

    pip install --upgrade sshreader

Contratulations!  You are now ready to begin working with sshreader!

Working With SSH Objects
------------------------

To start working with ssh connections (without multiprocessing or threading) right away.  Simply import the SSH class
and setup a connection!

.. code-block:: python

    from sshreader import SSH
    with SSH('myhost.example.com', username='jdoe', password='jdoe1') as s:
        uname = s.ssh_commaned('uname -a')
        print(uname)  # Show the results of the command, including stdin, stdout, and stderr

.. note::
    By using the :code:`with` statement you do not have to worry about running :code:`SSH.close()` when you are finished with
    an ssh connection.

Working with ServerJob Objects
------------------------------

ServerJob objects are a way to run multiple commands via ssh and return/tabulate the results.  ServerJobs can be placed
into a list and then processed using multiprocessing and multithreading via the :code:`sshreader.sshread()` method.

To create a ServerJob object and run it is nearly as simple as working with SSH objects:

.. code-block:: python

    from sshreader import ServerJob, sshread
    job1 = ServerJob('myhost.example.com',['uname -a', 'hostname', 'whoami'] username='jdoe', password='jdoe1')
    r = sshread(job1, tcount=0)
    print(r.status, r.results)

What happens here is that you create a ServerJob object that will run three commands in succession and record the results
in itself.  When you call :code:`sshread` you actually connect to the server and run the commands.

Working with Hook objects
-------------------------

Sometimes you want to run bits of code before or after a ServerJob executes as part of the :code:`sshread` method.
Sshreader provides a way to do this through :code:`Hook` objects.  Hook objects are simply a wrapper for a function you
have defined that will run before or after a ServerJob executes.  They will contain the ServerJob object itself as one of
the arguments so it is easy to write a Hook that can look at or react to the status of the ServerJob.

Creating a Hook is as is as simple as:

.. code-block:: python

    from sshreader import ServerJob, sshread, Hook

    def print_name(job):
        # You will need to ensure you accept at least one arg since
        # the ServerJob will be passed to your hook
        print('Entering hook')
        print(job.name)
        print('Leaving hook')


    # Create the function as a hook object
    myhook = Hook(target=print_name)
    # Create a ServerJob with a prehook
    job1 = ServerJob('myhost.example.com',['uname -a', 'hostname', 'whoami'] username='jdoe', password='jdoe1',
                     prehook=myhook)
    # Now, run the job
    sshread(job1)

Running Shell Commands
----------------------
Sometimes you don't want to run commands via ssh but want to run them in the shell on the localhost.  Sshreader provides
a method for doing that as well via the :code:`shell_command` method.

.. code-block:: python

    from sshreader import shell_command
    r = shell_command('uname -a')
    print(r)

Discovering Environment Variables
---------------------------------
Sshreader includes a method that attempts to determine the currently logged in username and any ssh keys located in
:code:`~/.ssh/`, including rsa and dsa keys.  You can see what sshreader can discover by calling the :code:`sshreader.ssh.envvars()`
method.

.. code-block:: python

    from sshreader.ssh import envvars
    print(envvars())  # Returns a NamedTuple of info sshreader was able to gather from the OS

Copying Files
-------------

Version 3.4 of sshreader introduced the :code:`SSH.sftp_put()` and :code:`SSH.sfpt_get()` methods into SSH objects.  These
methods attempt to make it easier to use Paramiko's SFTP protocol to copy files to and from a remote server.  The cool thing
about having them inside the SSH class is that you can use one object to both SFTP files and run SSH commands on a remote server.

.. code-block:: python

    from sshreader.ssh import SSH
    with SSH('myhost.example.com', username='jdoe', password='jdoe1') as s:
        # Copy a script file from our host to the remote host and run it.
        s.sftp_put('~/secret_script.sh', '/tmp/secret_script.sh')
        s.ssh_command('/tmp/secret_script.sh')
        # Now, get the output of the script and remove all traces of it
        s.sftp_get('/tmp/secret_output.txt', '~/secret_output.txt')
        s.ssh_command('rm /tmp/secret_output.txt', 'rm /tmp/secret_output.sh')

 .. note::

    Support for SFTP is new to sshreader and isn't a primary feature.  Support for this feature will be limited.

Indices and tables
------------------

* :ref:`sshreader`
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
* `JA Computing`_

.. _JA Computing: http://www.jacomputing.net