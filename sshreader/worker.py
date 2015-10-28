# coding=utf-8
""" Module for multi-threading/multiprocessing ServerJobs
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
from __future__ import print_function, division
import sys
from os import getpid
from multiprocessing import Process, cpu_count
from multiprocessing import Queue as processQueue
from threading import Thread
from Queue import Queue as threadQueue
from serverjob import _validate_hook_
from pkg_resources import get_distribution

__author__ = 'Jesse Almanrode (jesse@almanrode.com)'
__version__ = get_distribution('sshreader').version

tqueue = None
tcounter = 0
pqueue = None
finqueue = None
__jobHardLimit__ = (10 ** 6)
__cpuHardLimitFactor__ = 3
__previouspercentage__ = -1


class InvalidHook(Exception):
    """A pre or post hook definition is invalid
    """
    pass


class ProcessesOrThreads(Exception):
    """You did not specify whether to use subprocessing or threading
    """
    pass


class ExceededJobLimit(Exception):
    """Your number of jobs exceeds the current limit
    """
    pass


class ExceededCPULimit(Exception):
    """You have asked for more sub processes than your CPU is allowed to handle
    """
    pass


def progress_bar(progress, total, longbar=False):
    """Prints a syled progress bar

    - **parameters** and **return types**::

        :param progress: Current item number being processed
        :param total: Total number of items being processed
        :param longbar: Use a longer style progress bar
        :return: None
    """
    # TODO - Move to Click library
    global __previouspercentage__
    percent_float = float(progress) / float(total)
    percent = int(percent_float * 100)
    if __previouspercentage__ != percent:
        if longbar:
            hashes = "#" * percent
        else:
            hashes = "=" * int(percent/2)
            if percent % 2 != 0:
                hashes += "-"
        template = "[%s] %s%%" % (hashes, str(percent))
        if percent < 100:
            sys.stdout.write('\r' + template)
            sys.stdout.flush()
            __previouspercentage__ = percent
        else:
            __previouspercentage__ = -1
            print('\r' + template)
    return None


def tprint(message, stderr=False):
    """Attempt at a thread-safe print variation

    - **parameters** and **return types**::

        :param message: Message to output to stdout
        :param stderr: Message should go to stderr
        :return: None
    """
    # TODO - Can the print function be used here?
    if message.endswith('\n') is False:
        message += '\n'
    if stderr:
        sys.stderr.write(message)
        sys.stderr.flush()
    else:
        sys.stdout.write(message)
        sys.stdout.flush()
    return None


def sshread(serverjobs, debuglevel=0, pcount=None, tcount=None, progressbar=False, prehook=None, posthook=None):
    """Takes a list of serverJob objects and puts them into threads/subprocesses and runs them

    - **parameters** and **return types**::

        :param serverjobs: List of serverJob objects (A list of 1 job is acceptable)
        :param debuglevel: Debug level of all serverJobs (0 = off, 1 = some, 2 = more, 3 = all)
        :param pcount: Number of subprocesses to spawn (None = off, 0 = cpuSoftLimit, -1 = cpuHardLimit)
        :param tcount: Number of threads to spawn (None = off, 0 = adjusted length of serverJobList)
        :param progressbar: Print a progress bar
        :param prehook: Prehook for all serverJobs
        :param posthook: Posthook for all serverJobs
        :return: serverJobLst with completed serverJob objects (single object returned if single job passed)
    """
    if tcount is None and pcount is None:
        raise ProcessesOrThreads("You must specify a number for pcount or tcount!")
    if type(serverjobs) is not list:
        islist = False
        serverjobs = [serverjobs]
    else:
        islist = True
    totaljobs = len(serverjobs)

    # Per testing, don't allow more than 1 million jobs
    if totaljobs > __jobHardLimit__:
        print("The jobHardLimit for sshreader is: " + str(__jobHardLimit__))
        print("You are looking to process: " + str(totaljobs))
        raise ExceededJobLimit("Reached or exceeded jobHardLimit")

    # Figure out what globals we will need to apply to each serverJob object
    # before it is processed
    try:
        if int(debuglevel) <= 3:
            debuglevel = debuglevel
        else:
            raise TypeError("Debug level must be either 0, 1, 2, or 3")
    except:
        raise TypeError("Debug level must be an integer equal to 0, 1, 2, or 3")
    progressbar = progressbar
    if prehook is not None:
        prehook = _validate_hook_(prehook)
    if posthook is not None:
        posthook = _validate_hook_(posthook)

    if pcount is None:
        global tqueue, tcounter
        # Ensure the thread job counter is reset to 0
        tcounter = 0
        tqueue = threadQueue()
        # Fill up the Queue
        for thisJob in serverjobs:
            tqueue.put(thisJob)
        # Limit the number of threads to spawn
        if tcount == 0 or tcount > totaljobs:
            tcount = totaljobs

        # Start parent threads
        for pThread in xrange(tcount):
            if debuglevel >= 1:
                print("Spawning parent thread " + str(pThread))
            t = Thread(target=__tworker__, args=(debuglevel, prehook, posthook, progressbar, totaljobs))
            t.daemon = True
            t.start()

        # Wait for the queue to empty
        tqueue.join()

        if len(serverjobs) > 1 or islist:
            return serverjobs
        else:
            return serverjobs[0]
    else:
        global pqueue, finqueue
        pqueue = processQueue()
        finqueue = processQueue()
        # Load all but the current cpu on a box.
        cpusoftlimit = cpu_count() - 1
        # Imposing a hard limit for number of subprocesses so you don't make the system unusable
        cpuhardlimit = (cpusoftlimit * __cpuHardLimitFactor__)

        # Adjust number of subprocesses to spawn.
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

        # Add each serverJob object to the queue
        if tcount is None:
            for thisJob in serverjobs:
                pqueue.put(thisJob)
            subqueue = None
        else:
            # Set the number of threads for each subprocess to use
            # This could end up being smaller than what is set here
            # due to the number of items in the sub queues we are
            # about to set up.
            if tcount == 0 or tcount > totaljobs:
                tcount = totaljobs
            # Build a "sub queue" for each process to use
            subqueue = []
            subqueueitems = int(totaljobs / pcount)
            # Balance the totaljobs into subQueues for each subprocess
            while subqueueitems * pcount < totaljobs:
                subqueueitems += 1
            for x in xrange(0, totaljobs, subqueueitems):
                subqueue.append(serverjobs[x: x + subqueueitems])
            # If the balanced sub queue requires fewer processes, make it so
            if len(subqueue) < pcount:
                pcount = len(subqueue)

        # Start Parent processes for processing the Queue
        plist = []
        if debuglevel >= 2:
            print("Spawning " + str(pcount) + " subprocesses")
        for pID in xrange(pcount):
            if subqueue is None:
                p = Process(target=__pworker__, args=(debuglevel, prehook, posthook))
            else:
                p = Process(target=__sprocess__, args=(debuglevel, prehook, posthook, tcount, subqueue[pID]))
            plist.append(p)
            p.start()

        # Get the results from the Queue
        returnlist = []
        returnlen = len(returnlist)
        while returnlen < totaljobs:
            if progressbar:
                progress_bar(returnlen, totaljobs)
            # I think there is a bug with the following line that randomly causes pickle errors.
            # Not sure how to fix it.
            returnlist.append(finqueue.get())
            returnlen = len(returnlist)
        # This ensures that we print a final 100% progress bar
        if progressbar:
            progress_bar(returnlen, totaljobs)

        # Ensure all processes are closed
        for p in plist:
            p.join()

        # If we were passed a list then we will return a list
        if len(returnlist) > 1 or islist:
            return returnlist
        else:  # If an object, return an object
            return returnlist[0]


def print_results(serverjobs):
    """Print the output of all serverJobs in as serverJobList by status

    - **parameters** and **return types**::

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


def __pworker__(debuglevel, prehook, posthook):
    """This is a private method that is used by sshread to limit the number of processes sshreader spawns.

    DO NOT USE THIS METHOD! Use the sshread method instead!
    """
    global pqueue, finqueue
    pid = getpid()
    if debuglevel >= 1:
        print("Starting process: " + str(pid))
    while pqueue.empty() is False:
        thisjob = pqueue.get()
        thisjob.prehook = prehook
        thisjob.posthook = posthook
        thisjob.debuglevel = debuglevel
        thisjob.run()
        finqueue.put(thisjob)
    if debuglevel >= 1:
        print("Exiting process: " + str(pid))
    finqueue.close()
    return True


def __tworker__(debuglevel, prehook, posthook, progressbar, totaljobs):
    """This is a private method used to limit the number of threads that sshreader spawns.

    DO NOT USE THIS METHOD! Use the sshread method instead!
    """
    global tqueue, tcounter
    while True:
        thisjob = tqueue.get()
        thisjob.prehook = prehook
        thisjob.posthook = posthook
        thisjob.debuglevel = debuglevel
        cthread = Thread(target=thisjob.run)
        cthread.start()
        cthread.join()
        if progressbar:
            tcounter += 1
            progress_bar(tcounter, totaljobs)
        tqueue.task_done()


def __sprocess__(debuglevel, prehook, posthook, tcount, subqueue):
    """This is a private method used to have the multiprocessing and multithreading functionality combined.

    DO NOT USE THIS METHOD! Use the sshread method instead!
    """
    global finqueue, tqueue
    pid = getpid()
    if debuglevel >= 1:
        print("Starting process: " + str(pid))
    tqueue = threadQueue()
    for thisJob in subqueue:
        thisJob.prehook = prehook
        thisJob.posthook = posthook
        thisJob.debuglevel = debuglevel
        tqueue.put(thisJob)
    if tcount > len(subqueue):
        # Override the number of threads if it is greater than what we actually need
        tcount = len(subqueue)
    if debuglevel >= 2:
        print("Process " + str(pid) + " starting " + str(tcount) + " threads")
    for x in xrange(tcount):
        t = Thread(target=__sthread__)
        t.daemon = True
        t.start()
    tqueue.join()
    if debuglevel >= 1:
        print("Exiting process: " + str(pid))
    finqueue.close()
    return True


def __sthread__():
    """This is a private method used to have the multiprocessing and multithreading functionality combined.

    DO NOT USE THIS METHOD! Use the sshread method instead!
    """
    global tqueue, finqueue
    while tqueue.empty() is False:
        thisjob = tqueue.get()
        try:
            thisjob.run()
        except Exception as errMsg:
            print(errMsg)
        finqueue.put(thisjob)
        tqueue.task_done()
    return True
