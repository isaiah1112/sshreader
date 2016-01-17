# coding=utf-8
"""A Python Package for multi-processing/threading ssh connections in order to make ssh operations
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
method.

To use multi-processing to parallelize jobs either set **pcount** to 0 or to the number of processes you wish to spawn.
If the number of jobs is less than the number of processes you requested sshreader will adjust accordingly.  If
**pcount** is set to 0 then the number of processes spawned will equal *cpusoftlimit*.  If **pcount**
is set to -1 then the number of processes spawned will equal the *cpuhardlimit*.

When using **pcount** and **tcount** in conjunction, **tcount** will equal the total number of threads each process is
allowed to spawn.  Sshreader will automatically adjust the number of processes and number of threads in order to make
the execution of the jobs as efficient as possible.  These adjustments are done only in a reduction manor.  Thus, if the
number of jobs passed to :code:`sshreader.sshread()` method is less than the number of processes or threads requested
sshreader will adjust those numbers down automatically. Generally though, the total number of thread spawned when using
:code:`sshreader.sshread(pcount=0, tcount=0)` will equal:

.. code:: Python

    total_processes = cpusoftlimit
    total_threads = (total_processes * tcount)

Limits
------

**jobHardLimit**:

Sshreader currently limits you to processing :code:`1,000,000` server jobs set via the \_\_jobHardLimit\_\_ global.

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

.. [1] These numbers may increase in the future.
"""
# Copyright (C) 2015 Jesse Almanrode
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Lesser General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Lesser General Public License for more details.
#
#     You should have received a copy of the GNU Lesser General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import print_function, absolute_import
from pkg_resources import get_distribution, DistributionNotFound

# For backwards compatibility
from sshreader.ssh import SSH, shell_command, do_shell_script
from sshreader.sshreader import ServerJob, Hook, sshread, print_results

__author__ = 'Jesse Almanrode (jesse@almanrode.com)'
try:
    __version__ = get_distribution('sshreader').version
except DistributionNotFound:
    __version__ = 'UNKNOWN'
__all__ = ['sshreader', 'ssh']
