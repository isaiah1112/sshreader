.. sshreader documentation master file, created by
   sphinx-quickstart on Wed Oct 28 15:25:15 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _sshreader:

sshreader Package
=================

A Python Package for multi-processing/threading ssh connections in order to make ssh operations
across multiple servers parallel.  The module allows for timeouts for each ssh connection
as well as each command given to an ssh connection to run.  ServerJob objects allow for each server
to have multiple commands that should be run inside of a single job.  The results
from each job will be returned as a list of tuples inside of each ServerJob object in the same order that the
commands are sent in.

The SSH Module can also be used to create and call ssh connections without multiple processes/threads.

Sshreader can also run multi-processed/threaded shell commands on localhost and a serverJobList can contain both
serverJobs running on localhost as well as serverJobs running over ssh.

Threads vs. Processes vs. (Processes and Threads)
-------------------------------------------------

To use multi-threading to parallelize jobs either set **tcount** to 0 or to the number of threads you wish to spawn.
If the number of jobs is less than the number of threads you requested sshreader will adjust accordingly.  If **tcount**
is set to 0 then the number of threads spawned will either equal the number of jobs passed to the :code:`sshreader.sshread()`
method or the number returned from :code:`threadlimit()`, whichever is smaller.

To use multi-processing to parallelize jobs either set **pcount** to 0 or to the number of processes you wish to spawn.
If the number of jobs is less than the number of processes you requested sshreader will adjust accordingly.  If
**pcount** is set to 0 then the number of processes spawned will equal :code:`cpusoftlimit()`.  If **pcount**
is set to -1 then the number of processes spawned will equal the :code:`cpuhardlimit()`.

When using **pcount** and **tcount** in conjunction, **tcount** will equal the total number of threads each process is
allowed to spawn.  Sshreader will automatically adjust the number of processes and number of threads in order to make
the execution of the jobs as efficient as possible.  These adjustments are done only in a reduction manor.  Thus, if the
number of jobs passed to :code:`sshreader.sshread()` method is less than the number of processes or threads requested
sshreader will adjust those numbers down automatically. Generally though, the total number of thread spawned when using
:code:`sshreader.sshread(pcount=0, tcount=0)` will equal:

.. code:: Python

    total_processes = sshreader.cpusoftlimit()
    total_threads = min(len(jobs) // total_processes, threadlimit())

Topics
------

.. toctree::
   :maxdepth: 1

   getting_started
   faq
   pydsh
   testing

API Documentation
-----------------

.. toctree::
   :maxdepth: 1

   sshreader
   ssh

Compatibility
-------------

In order to maintain the widest range of compatibility, sshreader is currently tested using the following versions of
Python:

* Python3.4
* Python3.5
* Python3.6
* Python3.7
* Python3.8

.. note::

    As of version 5.0 of sshreader, Python2.7 is no longer supported in conjunction with
    the discontinuation of support for Python2.7 on January 1, 2020.  The last version
    to support Python2.7 is sshreader 4.5.

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
