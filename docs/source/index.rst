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
is set to 0 then the number of threads spawned will equal the number of jobs passed to the :code:`sshreader.sshread()`
method (without going over the *threadlimit* global).

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
    total_threads = (total_processes / jobs)

Limits
------

**jobHardLimit**:

Sshreader currently limits you to processing :code:`1,000,000` server jobs set via the \_\_jobHardLimit\_\_ global.

**threadlimit**:

Ssshreader will limit the number of threads each process can spawn to :code:`500` threads per the \_\_threadlimit\_\_ global.
This number will only take effect when tcount is set to 0.  If you manually specify tcount you can still launch as many
threads as you like.

**cpusoftlimit**:

The cpusoftlimit for a box is defined as:

.. code:: Python

    cpusoftlimit = (cpu_count() - 1)

This means that sshreader will spawn a sub-process for all but one cpu on a given box.

**cpuhardlimit**:

The cpuhardlimit is the maximum number of sub-processes that sshreader will spawn on a given box (when **pcount** is
set to -1) is defined as:

.. code:: Python

    cpuhardlimit = (cpusoftlimit * __cpuHardLimitFactor__)

This is so that you don't make a box unusable and was arrived at per my own testing.  Currently,
\_\_cpuHardLimitFactor\_\_ is set to 3 [1]_ .

Topics
------

.. toctree::
   :maxdepth: 1

   getting_started

API Documentation
-----------------

.. toctree::
   :maxdepth: 1

   sshreader
   ssh

Extras
------
.. toctree::
   :maxdepth: 1

   pydsh
   faq

Compatibility
-------------

As of version 3.0, sshreader now supports both Python 2.7 and 3.5.

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. [1] These numbers may increase in the future.