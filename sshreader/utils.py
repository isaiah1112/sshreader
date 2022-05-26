# coding=utf-8
""" All the classes and functions that make sshreader tick
"""
# Copyright (C) 2015-2022 Jesse Almanrode
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
from collections import namedtuple
from progressbar import ProgressBar
from sshreader.ssh import SSH
from sshreader.types import Command, TimeoutTuple
from types import FunctionType
from typing import Any, Callable, Optional, Union
import logging
import multiprocessing
import os
import paramiko
import subprocess
import sys
import threading
import time

if sys.version_info[0] < 3:
    raise Exception('Python2.x is no longer supported in this version of sshreader')
elif sys.version_info[1] < 7:
    raise Exception('Only Python 3.7 and later is supported in this version of sshreader')


# Globals
__author__ = 'Jesse Almanrode (jesse@almanrode.com)'
mpctx = multiprocessing.get_context('spawn')  # Forcing the forking type to spawn in older versions of Python3
__cpuhardlimitfactor__ = 3
__threadlimitfactor__ = 2
log = logging.getLogger('sshreader')
lockobj = None

def shell_command(command: str, combine: bool = False, decodebytes: bool = True) -> Command:
    """Run a command in the shell on localhost and return the output

    :param command: The shell script to run
    :type command: str, required
    :param combine: Direct stderr to stdout (Default: False)
    :type combine: bool, optional
    :param decodebytes: Decode bytes objects to unicode strings (Default: True)
    :type decodebypes: bool, optional
    :return: NamedTuple for (cmd, stdout, stderr) or (cmd, stdout)
    :rtype: Command
    :raises: None
    """
    global log
    log.warning('%s is being deprecated, please use %s instead' % (str(shell_command), str(subprocess.run)))
    if combine:
        sp_output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if decodebytes:
            result = Command(cmd=command, stdout=sp_output.stdout.decode(), stderr=None,
                             return_code=sp_output.returncode)
        else:
            result = Command(cmd=command, stdout=sp_output.stdout, stderr=None, return_code=sp_output.returncode)
    else:
        sp_output = subprocess.run(command, shell=True, capture_output=True)
        if decodebytes:
            result = Command(cmd=command, stdout=sp_output.stdout.decode(), stderr=sp_output.stderr.decode(),
                             return_code=sp_output.returncode)
        else:
            result = Command(cmd=command, stdout=sp_output.stdout, stderr=sp_output.stderr.decode(),
                             return_code=sp_output.returncode)
    return result


class Hook(object):
    """ Custom class for pre and post hooks

    :param target: Function to call when using the hook
    :type target: func, required
    :param args: List of args to pass to target function
    :type args: list, optional
    :param kwargs: Dictionary of keyword arguments to pass to target function
    :type kwargs: dict, optional
    :param ssh_established: Should the ssh connection be established when the hook is run (Default: False)
    :type ssh_established: bool, optional
    :raises: TypeError
    """

    def __init__(self, target: Callable, args: Optional[list] = None, kwargs: Optional[dict] = None,
                 ssh_established: bool = False) -> None:
        assert isinstance(target, FunctionType)
        self.target = target
        self.ssh_established = ssh_established
        if args is None:
            self.args = list()
        else:
            assert isinstance(args, list)
            self.args = args
        if kwargs is None:
            self.kwargs = dict()
        else:
            assert isinstance(kwargs, dict)
            self.kwargs = kwargs
        self.result = None

    def run(self, *args, **kwargs) -> Any:
        """ Run the Hook.  You can add additional args or kwargs at this time!

        :param args: Append to args
        :type args: list, optional
        :param kwargs: Append to/update kwargs
        :type kwargs: dict, optional
        :return: Result from :obj:`target` function
        """
        # I perform the following actions this way specifically so I don't "update" the pre-defined args and kwargs
        # in the Hook object.
        args = self.args + list(args)
        kwargs = dict(list(self.kwargs.items()) + list(kwargs.items()))
        self.result = self.target(*args, **kwargs)
        return self.result

    def __str__(self) -> str:
        return str(self.__dict__)


class ServerJob(object):
    """ Custom class for holding all the info needed to run ssh commands or shell commands in sub-processes or threads

    :param fqdn: Fully qualified domain name or IP address
    :type fqdn: str, required
    :param cmds: List of commands to run (in the order you want them run)
    :type cmds: list, required
    :param username: Username for SSH
    :type username: str, optional
    :param password: Password for SSH
    :type password: str, optional
    :param keyfile: Path to ssh private key
    :type keyfile: str, optional
    :param keypass: Password for private ssh key file
    :type keypass: str, optional
    :param timeout: Tuple of timeouts in seconds (TCP timeout, SSH Timeout)
    :type timeout: tuple, optional
    :param runlocal: Run job on localhost without opening SSH connection (Default: False)
    :type runlocal: bool, optional
    :param prehook: Hook object
    :type prehook: :class:`Hook`, optional
    :param posthook: Hook object
    :type posthook: :class:`Hook`, optional
    :param combine_output: Combine stdout and stderr (Default: False)
    :type combine_output: bool, optional

    :property results: List of namedtuples (cmd, stdout, stderr, return_code) or (cmd, stdout, return_code)
    :property status: Sum of return codes for entire job (255 = ssh did not connect)
    """
    def __init__(self, fqdn: str, cmds: Union[list, tuple, str], username: Optional[str] = None,
                 password: Optional[str] = None, keyfile: Optional[str] = None, keypass: Optional[str] = None,
                 timeout: Optional[TimeoutTuple] = (0.5, 30), runlocal: bool = False,
                 prehook: Optional[Callable] = None, posthook: Optional[Callable] = None,
                 combine_output: bool = False) -> None:
        self.name = str(fqdn)
        self.results = list()
        self.username = username
        self.password = password
        self.key = keyfile
        self.keypass = keypass
        self.status = 0
        self.combine_output = combine_output
        self.runlocal = runlocal
        self.ssh_port = 22
        if isinstance(cmds, (list, tuple)):
            self.cmds = cmds
        else:
            self.cmds = [cmds]
        if isinstance(timeout, (tuple, list)):
            if len(timeout) != 2:
                raise ValueError('<timeout> requires two integer or float values')
            assert isinstance(timeout[0], (int, float))
            assert isinstance(timeout[1], (int, float))
            self.sshtimeout = timeout[0]
            self.cmdtimeout = timeout[1]
        else:
            assert isinstance(timeout, (int, float))
            self.sshtimeout = timeout
            self.cmdtimeout = timeout
        if prehook:
            if isinstance(prehook, Hook):
                self.prehook = prehook
            else:
                raise TypeError('prehook should be of type: ' + str(Hook))
        else:
            self.prehook = prehook
        if posthook:
            if isinstance(posthook, Hook):
                self.posthook = posthook
            else:
                raise TypeError('posthook should be of type: ' + str(Hook))
        else:
            self.posthook = posthook
        if runlocal:
            self._conn = 'localhost'
        elif not keyfile and len(paramiko.Agent().get_keys()) == 0:
            if not all([username, password]):
                raise paramiko.SSHException('username and password or ssh key not provided')

    def run(self) -> int:
        """Run a ServerJob. SSH to server, run cmds, return result

        :return: Sum of return codes for each command executed
        :rtype: int
        """
        log.info('%s: starting ServerJob' % (self.name,))
        if self.runlocal:
            if self.prehook:
                log.debug('%s: running prehook' % (self.name,))
                self.prehook.run(self)
            for cmd in self.cmds:
                result = shell_command(cmd, combine=self.combine_output)
                log.debug('%s: %s' % (self.name, str(result)))
                self.results.append(result)
                self.status += result.return_code
            if self.posthook:
                log.debug('%s; running posthook' % (self.name,))
                self.posthook.run(self)
        else:
            if self.prehook and self.prehook.ssh_established is False:
                log.debug('%s: running prehook' % (self.name,))
                self.prehook.run(self)
            try:
                self._conn = SSH(self.name, username=self.username, password=self.password, keyfile=self.key,
                                 port=self.ssh_port, connect=False)
                self._conn.connect(timeout=self.sshtimeout)
                log.debug('%s: ssh connection established' % (self.name,))
            except Exception as errorMsg:
                log.debug(str(errorMsg))
                self.status = 255
                self.results.append(str(errorMsg))
            else:
                if self.prehook and self.prehook.ssh_established:
                    log.debug('%s: running prehook' % (self.name,))
                    self.prehook.run(self)
                for cmd in self.cmds:
                    try:
                        result = self._conn.ssh_command(cmd, timeout=self.cmdtimeout, combine=self.combine_output)
                    except Exception as errorMsg:
                        result = Command(cmd, '', str(errorMsg), 54)
                    log.debug('%s: %s' % (self.name, str(result)))
                    self.results.append(result)
                    self.status += result.return_code
                if self.posthook and self.posthook.ssh_established:
                    log.debug('%s; running posthook' % (self.name,))
                    self.posthook.run(self)
                self._conn.close()
            finally:
                self._conn = None  # So the ssh connection can be pickled!
            if self.posthook and self.posthook.ssh_established is False:
                log.debug('%s; running posthook' % (self.name,))
                self.posthook.run(self)
        log.info('%s: exiting ServerJob' % (self.name,))
        return self.status

    def __str__(self) -> str:
        return str(self.__dict__)

    def __getitem__(self, item):
        return self.__dict__[item]


def cpusoftlimit() -> int:
    """ Using the cpu count, determine number of processes the script is allowed to spawn

    :return: Result of :meth:`mpctx.cpu_count()` or 1, whichever is greater
    :rtype: int
    """
    cpu_count = mpctx.cpu_count()
    if cpu_count > 1:
        return cpu_count - 1
    else:
        return cpu_count


def cpuhardlimit() -> int:
    """ Return the maximum number of sub-processes your system is allowed to spawn.

    :return: cpusoftlimit() * __cpuhardlimitfactor__
    :rtype: int
    """
    global __cpuhardlimitfactor__
    assert isinstance(__cpuhardlimitfactor__, int)
    return cpusoftlimit() * __cpuhardlimitfactor__


def threadlimit() -> int:
    """ Return the maximum number of threads each process is allowed to spawn.  The idea here is to not overload a system.

    :return: cpu_count() * __threadlimitfactor__
    :rtype: int
    """
    global __threadlimitfactor__
    assert isinstance(__threadlimitfactor__, int)
    return mpctx.cpu_count() * __threadlimitfactor__


def echo(*args, **kwargs) -> None:
    """ Wrapper for print that implements a :class:`multiprocessing.Lock` object as well as uses unbuffered output
    to :class:`sys.stdout`.

    :param args: Passthrough to print function
    :param kwargs: Passthrough to print function
    :return: None
    :rtype: None
    """
    global lockobj
    if lockobj:
        with lockobj:
            print(*args, **kwargs)
    else:
        print(*args, **kwargs)
    sys.stdout.flush()
    return None


def sshread(serverjobs: list, pcount: Optional[int] = None, tcount: Optional[int] = None,
            progress_bar: bool = False, print_lock: bool = True) -> list:
    """Takes a list of ServerJob objects and puts them into threads/sub-processes and runs them

    :param serverjobs: List of ServerJob objects
    :type serverjobs: list, required
    :param pcount: Number of sub-processes to spawn (None = off, 0 = cpusoftlimit, -1 = cpuhardlimit)
    :type pcount: int, required
    :param tcount: Number of threads to spawn (None = off, 0 = threadlimit)
    :type tcount: int, required
    :param progress_bar: Print a progress bar (Default: False)
    :type progress_bar: bool, optional
    :param print_lock: Create a :class:multiprocessing.Lock for use with :meth:`sshreader.echo()`
    :type print_lock: bool, optional
    :return: List of completed ServerJob objects (single object returned if 1 job was passed)
    :rtype: list
    :raises: ExceedCPULimit, TypeError, ValueError
    """
    global lockobj
    assert isinstance(serverjobs, list)
    if tcount is None and pcount is None:
        raise ValueError('tcount or pcount must be ' + str(int))
    if tcount is not None:
        assert isinstance(tcount, int)
    if pcount is not None:
        assert isinstance(pcount, int)
    totaljobs = len(serverjobs)

    if logging.getLogger('sshreader').getEffectiveLevel() < 30 and progress_bar:
        log.info('logging enabled: disabling progress bar')
        progress_bar = False

    if progress_bar:
        item_counter = mpctx.Value('L', 0)
        bar = ProgressBar(max_value=totaljobs)
    else:
        item_counter = None
        bar = None

    if print_lock:
        lockobj = mpctx.Lock()

    task_queue = mpctx.Queue(maxsize=totaljobs)
    result_queue = mpctx.Queue(maxsize=totaljobs)

    log.debug('filling task_queue')
    for job in serverjobs:
        task_queue.put(job)

    threads = list()  # Keep track of threads so we can join them later
    pids = list()  # Keep track of process-ids so we can join/close them later

    if pcount is None:
        # Limit the number of threads to spawn
        if tcount == 0:
            tcount = int(min(totaljobs, threadlimit()))
        else:
            tcount = int(min(tcount, totaljobs))

        log.info(u'spawning %d threads' % (tcount, ))
        # Start a thread pool
        for thread in range(tcount):
            thread = threading.Thread(target=_sub_thread_, args=(task_queue, result_queue, item_counter, progress_bar),
                                      daemon=True)
            thread.start()
            threads.append(thread)
    else:
        # Found this while digging around the multiprocessing API.
        # This might help some of the pickling errors when working with ssh
        mpctx.allow_connection_pickling()

        # Adjust number of sub-processes to spawn.
        if pcount == 0:
            pcount = cpusoftlimit()
        elif pcount < 0:
            pcount = cpuhardlimit()
        pcount = int(min(pcount, totaljobs))

        if pcount > cpuhardlimit():
            raise ValueError('CPUHardLimit exceeded: %d > %d' % (pcount, cpuhardlimit()))

        if tcount is None:
            tcount = 0
        else:
            if tcount == 0:
                tcount = int(min(totaljobs // pcount, threadlimit()))
            if tcount < 2:
                # If we don't have enough jobs to spawn more than 1 thread per process, then we won't spawn threads
                tcount = 0

        log.info(u'spawning %d processes' % (pcount, ))
        for pid in range(pcount):
            pid = mpctx.Process(target=_sub_process_, args=(task_queue, result_queue, item_counter, tcount, progress_bar),
                                daemon=True)
            pid.start()
            pids.append(pid)

    # Non blocking way to wait for threads/processes
    log.debug('main waiting for %d ServerJobs to finish' % (totaljobs,))
    while result_queue.full() is False:
        if progress_bar:
            bar.update(item_counter.value)
        time.sleep(1)
    if progress_bar:
        bar.finish()

    if len(threads) > 0:
        log.info('joining %d threads' % (len(threads),))
        for t in threads:
            if t.is_alive():
                t.join(timeout=1)
    elif len(pids) > 0:
        log.info('joining %d processes' % (len(pids),))
        for p in pids:
            if p.is_alive():
                p.join(timeout=1)
            p.close()

    # Extract items from the queue and return a list, just as we were passed
    results = list()
    while not result_queue.empty():
        results.append(result_queue.get())
    task_queue.close()
    result_queue.close()
    return results


def _sub_process_(task_queue, result_queue, item_counter, thread_count, progress_bar):
    """ Private method for managing multi-processing and spawning thread pools.

    DO NOT USE THIS METHOD!
    """
    pid = os.getpid()
    log.debug(u'starting process: %d' % (pid,))
    if thread_count == 0:
        while task_queue.empty() is False:
            job = task_queue.get()
            job.run()
            result_queue.put(job)
            if progress_bar:
                with item_counter.get_lock():
                    item_counter.value += 1
    else:
        threads = list()
        log.debug(u'process: %d spawning: %d threads' % (pid, thread_count))
        for thread in range(thread_count):
            thread = threading.Thread(target=_sub_thread_, args=(task_queue, result_queue, item_counter, progress_bar),
                                      daemon=True)
            thread.start()
            threads.append(thread)
        log.debug(u'process: %d waiting for: %d threads' % (pid, len(threads)))
        for thread in threads:
            thread.join()
    log.debug(u'exiting process: %d' % (pid,))
    return None


def _sub_thread_(task_queue, result_queue, item_counter, progress_bar):
    """ Private method for managing multi-processing and spawning thread pools.

    DO NOT USE THIS METHOD!
    """
    log.debug('entering thread')
    while task_queue.empty() is False:
        job = task_queue.get()
        job.run()
        result_queue.put(job)
        if progress_bar:
            with item_counter.get_lock():
                item_counter.value += 1
    log.debug('existing thread')
    return None
