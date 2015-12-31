# coding=utf-8
""" All the classes and functions that make sshreader tick
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
from __future__ import absolute_import, print_function, division
import os
import paramiko
import multiprocessing
import threading
import queue
import warnings
from builtins import range  # Replaces xrange in Python2
from types import FunctionType
from sshreader.ssh import SSH, do_shell_script
from progressbar import ProgressBar

__author__ = 'Jesse Almanrode (jesse@almanrode.com)'

separator = "-" * 10
__jobHardLimit__ = (10 ** 6)
__cpuHardLimitFactor__ = 3


class InvalidHook(Exception):
    """ A pre or post hook definition is invalid
    """
    pass


class ProcessesOrThreads(Exception):
    """ You did not specify whether to use sub-processing or threading
    """
    pass


class ExceededJobLimit(Exception):
    """ Your number of jobs exceeds the current limit
    """
    pass


class ExceededCPULimit(Exception):
    """ You have asked for more sub processes than your CPU is allowed to handle
    """
    pass


class InvalidArgument(Exception):
    """ An invalid argument was passed to a function
    """
    pass


class Hook(object):
    """ Custom class for pre and post hooks

    :param target: Function to call when using the hook
    :param args: List of args to pass to target
    :param kwargs: Dictionary of kwargs to pass to target
    :return: Hook
    """

    def __init__(self, target, args=None, kwargs=None):
        if isinstance(target, FunctionType):
            self.target = target
        else:
            raise InvalidArgument('target should be of type: <function>')
        if args is None:
            self.args = list()
        else:
            if isinstance(args, list):
                self.args = args
            else:
                raise InvalidArgument('args should be of type: <list>')
        if kwargs is None:
            self.kwargs = dict()
        else:
            if isinstance(kwargs, dict):
                self.kwargs = kwargs
            else:
                raise InvalidArgument('kwargs should be of type: <dict>')
        self.result = None

    def run(self, *args, **kwargs):
        """ Run the Hook.

        :param args: Override args
        :param kwargs: Override kwargs
        :return: Result from target function
        """
        if len(args) == 0:
            args = self.args
        if len(kwargs) == 0:
            kwargs = self.kwargs
        self.result = self.target(*args, **kwargs)
        return self.result


class ServerJob(object):
    """ Custom class for holding all the info needed to run ssh commands or shell commands in sub-processes or threads

    :param fqdn: Fully qualified domain name or IP address
    :param cmds: List of commands to run (in the order you want them run)
    :param username: Username for SSH
    :param password: Password for SSH
    :param keyfile: Path to ssh key (can be used instead of password)
    :param debuglevel: 0 = off, 1 = some, 2 = more, 3 = all
    :param timeout: Tuple of timeouts (sshtimeout, cmdtimeout), if not specified both default to 30 seconds
    :param runlocal: Run job on localhost (skips ssh to localhost)
    :param prehook: Optional Hook object
    :param posthook: Optional Hook object
    :return: serverJob Object

    :property cmdResults: List of results of each command in tuple form (cmd, stdout, stderr)
    :property cmdStatus: List of states for each command ( None = initial state/cmd did not run, True = no stderr,
                        False = stderr)
    :property status: State of entire job (None = initial state/ssh failed, True = all cmd statuses is True,
                        False = one or more cmd statuses is False)
    :property combine_output: Combine stdout and stderr in cmdResults (default = False)
    """
    def __init__(self, fqdn, cmds, username=None, password=None, keyfile=None, debuglevel=0, timeout=(30, 30),
                 runlocal=False, prehook=None, posthook=None):
        if isinstance(cmds, (list, tuple)):
            self.cmds = cmds
        else:
            self.cmds = [cmds]
        self.cmdResults = []
        self.cmdStatus = []
        self.username = username
        self.password = password
        self.key = keyfile
        self.status = None
        if isinstance(timeout, (tuple, list)):
            if len(timeout) != 2:
                raise InvalidArgument('You must supply two timeouts if you pass a tuple or list')
            self.sshtimeout = timeout[0]
            self.cmdtimeout = timeout[1]
        else:
            self.sshtimeout = timeout
            self.cmdtimeout = timeout
        self.runlocal = runlocal
        self.name = fqdn
        if prehook is not None:
            if isinstance(prehook, Hook):
                self.prehook = prehook
            else:
                raise InvalidArgument('prehook should be of type: <Hook>')
        else:
            self.prehook = prehook
        if posthook is not None:
            if isinstance(posthook, Hook):
                self.posthook = posthook
            else:
                raise InvalidArgument('prehook should be of type: <Hook>')
        else:
            self.posthook = posthook
        self.combine_output = False
        try:
            if int(debuglevel) <= 3:
                self.debuglevel = debuglevel
            else:
                raise TypeError("Debug level must be an integer between 0 and 3")
        except TypeError:
            raise TypeError("Debug level must be an integer between 0 and 3")
        if runlocal is False:
            self.ssh_con = None
            if keyfile is None:
                if username is None or password is None:
                    raise paramiko.SSHException("You must enter a username and password or supply an SSH key")
                else:
                    self.keyauth = False
            else:
                self.keyauth = True
        else:
            self.ssh_con = "localhost"

    def run(self):
        """Run a serverJob. SSH to server, run cmds, return result

        :return: serverJob.status
        """
        if self.debuglevel >= 1:
            print("Running serverJob: " + self.name)
        # Run prehook if it is defined
        if self.prehook is not None:
            if self.debuglevel >= 2:
                print("Running prehook")
            self.prehook.args.append(self)
            self.prehook.run()
            self.prehook.args.remove(self)
        # Establish SSH Connection if we are not working locally
        if self.runlocal is False:
            try:
                if self.keyauth:
                    if self.username is None:
                        self.ssh_con = SSH(self.name, keyfile=self.key, timeout=self.sshtimeout)
                    else:
                        self.ssh_con = SSH(self.name, username=self.username, keyfile=self.key, timeout=self.sshtimeout)
                else:
                    self.ssh_con = SSH(self.name, username=self.username, password=self.password,
                                       timeout=self.sshtimeout)
            except Exception as errorMsg:
                if self.debuglevel >= 2:
                    print(errorMsg)
                self.ssh_con = None
                if self.debuglevel >= 1:
                    print(self.name + ": Unable to establish ssh connection!")
        # This is a trick statement to allow ssh and local shell scripts to be run using similar output processing code
        if self.ssh_con is not None:
            for idX, thiscmd in enumerate(self.cmds):
                # Now running each command in turn
                self.cmdStatus.append(None)
                if self.debuglevel >= 3:
                    print(self.name + " running: " + thiscmd)
                if self.runlocal:
                    if self.combine_output:
                        result = do_shell_script(thiscmd, combine=True)
                    else:
                        result = do_shell_script(thiscmd)
                else:
                    if self.combine_output:
                        result = self.ssh_con.ssh_command(thiscmd, timeout=self.cmdtimeout, combine=True)
                    else:
                        result = self.ssh_con.ssh_command(thiscmd, timeout=self.cmdtimeout)
                self.cmdResults.append(result)
                if self.combine_output:
                    # We are combining stdout and stderr
                    self.cmdStatus[idX] = True
                else:
                    if len(result[2]) == 0:
                        # No stderr output
                        self.cmdStatus[idX] = True
                    else:
                        # Something was output to stdError
                        self.cmdStatus[idX] = False
                if self.debuglevel >= 3:
                    print(self.name + ": " + thiscmd + ": Finished")
            if False in self.cmdStatus or None in self.cmdStatus:
                self.status = False
            else:
                self.status = True
            # Close ssh connection if needed
            if self.runlocal is False:
                self.ssh_con.close()
            self.ssh_con = None
            # Run post hook before we are done with this job
        if self.posthook is not None:
            if self.debuglevel >= 2:
                print("Running posthook")
            self.posthook.args.append(self)
            self.posthook.run()
            self.posthook.args.remove(self)
        if self.debuglevel >= 1:
            print("Finished running serverJob: " + self.name)
        return self.status

    def print_results(self, printname=False):
        """Prints the command run and its output

        :param printname: Print the serverJob name
        :return: None
        """
        if printname:
            print("serverJob: " + self.name + "\n" + (separator*3))
        for idx, value in enumerate(self.cmds):
            print(value + ":\n" + ";".join(self.cmdResults[idx]) + "\n" + separator)
        return None

    def __str__(self):
        return str(self.__dict__)

    def __getitem__(self, item):
        return self.__dict__[item]

    def keys(self):
        """So you can work with the object in Dictionary form
        """
        return self.__dict__.keys()


def print_results(serverjobs):
    """Print the output of all serverJobs in as serverJobList by status

    :param serverjobs: A list of sshreaded serverJob objects
    :return: None
    """
    nonestatus = [x for x in serverjobs if x.status is None]
    completejobs = [x for x in serverjobs if x.status is True]
    errorjobs = [x for x in serverjobs if x.status is False]
    if len(completejobs) > 0:
        print("\nSUCCESSFUL SERVERJOBS\n")
        for x in completejobs:
            x.print_results(True)
    if len(errorjobs) > 0:
        print("\nERRORED SERVERJOBS\n")
        for x in errorjobs:
            x.print_results(True)
    if len(nonestatus) > 0:
        print("\nINCOMPLETE SERVERJOBS\n")
        for x in nonestatus:
            x.print_results(True)
    return None


def sshread(serverjobs, debuglevel=0, pcount=None, tcount=None, progress_bar=False):
    """Takes a list of serverJob objects and puts them into threads/sub-processes and runs them

    :param serverjobs: List of serverJob objects (A list of 1 job is acceptable)
    :param debuglevel: Debug level for threads/processes (0 = off, 1 = some, 2 = more, 3 = all)
    :param pcount: Number of sub-processes to spawn (None = off, 0 = cpuSoftLimit, -1 = cpuHardLimit)
    :param tcount: Number of threads to spawn (None = off, 0 = adjusted length of serverJobList)
    :param progress_bar: Print a progress bar
    :return: serverJobLst with completed serverJob objects (single object returned if single job passed)
    """
    if tcount is None and pcount is None:
        raise ProcessesOrThreads("You must specify a number for pcount or tcount!")
    if isinstance(serverjobs, list):
        islist = True
    else:
        islist = False
        serverjobs = [serverjobs]
    totaljobs = len(serverjobs)

    # Per testing, don't allow more than 1 million jobs
    if totaljobs > __jobHardLimit__:
        print("The jobHardLimit for sshreader is: " + str(__jobHardLimit__))
        print("You are looking to process: " + str(totaljobs))
        raise ExceededJobLimit("Reached or exceeded jobHardLimit")

    try:
        if int(debuglevel) <= 3:
            debuglevel = debuglevel
        else:
            raise TypeError("Debug level must be either 0, 1, 2, or 3")
    except:
        raise TypeError("Debug level must be an integer equal to 0, 1, 2, or 3")

    if debuglevel > 0 and progress_bar:
        progress_bar = False
        warnings.warn('You should not use progress_bar and debuglevel together. Silencing progress_bar.')

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')  # For Python3
        item_counter = multiprocessing.Value('L', 1)
    if progress_bar:
        bar = ProgressBar(max_value=totaljobs)
    else:
        bar = None

    if pcount is None:
        task_queue = queue.Queue(maxsize=totaljobs)
        result_queue = queue.Queue(maxsize=totaljobs)
        # Fill up the Queue
        for job in serverjobs:
            task_queue.put(job)
        # Limit the number of threads to spawn
        if tcount == 0 or tcount > totaljobs:
            tcount = totaljobs

        if debuglevel >= 1:
            print("Spawning " + str(tcount) + " threads")
        # Start a thread pool
        for thread in range(tcount):
            if debuglevel >= 2:
                print("Spawning: Thread-" + str(thread))
            thread = threading.Thread(target=_sub_thread_, args=(task_queue, result_queue, item_counter))
            thread.daemon = True
            thread.start()
    else:
        # Limit the number of sub processes we spawn
        cpusoftlimit = multiprocessing.cpu_count() - 1
        # Imposing a hard limit for number of sub-processes so you don't make the system unusable
        cpuhardlimit = cpusoftlimit * __cpuHardLimitFactor__

        # Adjust number of sub-processes to spawn.
        if pcount == 0:
            pcount = cpusoftlimit
        elif pcount < 0:
            pcount = cpuhardlimit
        if pcount >= totaljobs:
            pcount = totaljobs

        if pcount > cpuhardlimit:
            print("The cpuHardLimit for your system is: " + str(cpuhardlimit))
            print("You asked for: " + str(pcount))
            raise ExceededCPULimit("Reached or exceeded cpuHardLimit")

        if tcount is not None:
            if tcount == 0:
                tcount = totaljobs // pcount
                if tcount <= 1:
                    tcount = None

        task_queue = multiprocessing.Queue(maxsize=totaljobs)
        result_queue = multiprocessing.Queue(maxsize=totaljobs)

        # Add each serverJob object to the queue
        for job in serverjobs:
            task_queue.put(job)

        if debuglevel >= 1:
            print("Spawning " + str(pcount) + " sub-processes")
        for pid in range(pcount):
            pid = multiprocessing.Process(target=_sub_process_, args=(task_queue, result_queue, item_counter),
                                          kwargs={'thread_count': tcount, 'debuglevel': debuglevel})
            pid.daemon = True
            pid.start()

    # Non blocking way to wait for threads/processes
    while result_queue.full() is False:
        if progress_bar:
            bar.update(item_counter.value)

    completed_jobs = list()
    while result_queue.empty() is False:
        completed_jobs.append(result_queue.get())
    # If we were passed a list then we will return a list
    if len(completed_jobs) > 1 or islist:
        return completed_jobs
    else:  # If an object, return an object
        return completed_jobs[0]


def _sub_process_(task_queue, result_queue, item_counter, thread_count=None, debuglevel=0):
    """ Private method for managing multi-processing and spawning thread pools.

    DO NOT USE THIS METHOD!
    """
    pid = os.getpid()
    if debuglevel >= 2:
        print("Starting process: " + str(pid))
    if thread_count is None:
        while task_queue.empty() is False:
            job = task_queue.get()
            job.run()
            result_queue.put(job)
            with item_counter.get_lock():
                item_counter.value += 1
    else:
        if debuglevel >= 1:
            print("Process: " + str(pid) + " spawning: " + str(thread_count) + " threads")
        for thread in range(thread_count):
            if debuglevel >= 2:
                print("Process: " + str(pid) + " spawning: Thread-" + str(thread))
            thread = threading.Thread(target=_sub_thread_, args=(task_queue, result_queue, item_counter))
            thread.daemon = True
            thread.start()
        while threading.active_count() > 1:
            pass
    if debuglevel >= 2:
        print("Exiting process: " + str(pid))
    return None


def _sub_thread_(task_queue, result_queue, item_counter):
    """ Private method for managing multi-processing and spawning thread pools.

    DO NOT USE THIS METHOD!
    """
    while task_queue.empty() is False:
        job = task_queue.get()
        job.run()
        result_queue.put(job)
        with warnings.catch_warnings():  # For python3
            warnings.simplefilter('ignore')
            with item_counter.get_lock():
                item_counter.value += 1
    return None
