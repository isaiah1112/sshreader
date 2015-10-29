#!/usr/bin/env python
# coding=utf-8
"""All the classes contained in sshreader, including ServerJob, SSH, and exception classes
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
from __future__ import print_function
import paramiko
import logging
from types import FunctionType
from pkg_resources import get_distribution
from functions import do_shell_script

__author__ = 'Jesse Almanrode (jesse@almanrode.com)'
__version__ = get_distribution('sshreader').version
separator = "---------"


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


class InvalidArgument(Exception):
    """An invalid argument was passed to a function
    """
    pass


class SSH(object):
    """SSH Session object

    - **parameters** and **return types**::

        :param fqdn: Fully qualified domain name or IP address
        :param username: SSH username
        :param password: SSH password
        :param keyfile: SSH keyfile (can be used instead of password)
        :param port: SSH port (default = 22)
        :param timeout: SSH connection timeout in seconds (default = 30)
        :return: SSH connection object
    """
    def __init__(self, fqdn, username=None, password=None, keyfile=None, port=22, timeout=30):
        self.__host__ = fqdn
        self.__username__ = username
        self.__password__ = password
        self.__keyfile__ = keyfile
        self.__port__ = port
        self.__timeout__ = timeout
        self.connection = paramiko.SSHClient()
        self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.connect()

    def ssh_command(self, command, timeout=30, combine=False):
        """Run a command over an ssh connection

        - **parameters** and **return types**::

            :param command: The command to run
            :param timeout: Timeout for the command
            :param combine: Combine stderr and stdout
            :return: Tuple of (command, stdout, stderr) or (command, output)
        """
        if combine:
            stdin, stdout = self.connection.exec_command(command, timeout=timeout, get_pty=True)
            return command, stdout.read().strip()
        else:
            stdin, stdout, stderr = self.connection.exec_command(command, timeout=timeout)
            return command, stdout.read().strip(), stderr.read().strip()

    def close(self):
        """Closes an established ssh connection
        """
        self.connection.close()
        return None

    def is_alive(self):
        """Is an SSH connection alive
        """
        if self.connection.get_transport() is None:
            return False
        else:
            if self.connection.get_transport().is_alive():
                return True
            else:
                raise paramiko.SSHException("Unable to determine state of ssh session")

    def reconnect(self):
        """Alias to connect
        """
        self.connect()

    def connect(self):
        """Opens an SSH Connection
        """
        # http://stackoverflow.com/questions/26659772/silence-no-handlers-could-be-found-for-logger-paramiko-transport-message
        logging.basicConfig()
        if self.is_alive():
            raise paramiko.SSHException("Connection is already established")
        # Per http://stackoverflow.com/questions/19152578/no-handlers-could-be-found-for-logger-paramiko
        if self.__keyfile__ is not None:
            if self.__username__ is not None:  # Key file with a custom username!
                self.connection.connect(self.__host__, port=self.__port__, username=self.__username__,
                                        key_filename=self.__keyfile__, timeout=self.__timeout__, look_for_keys=False)
            else:
                self.connection.connect(self.__host__, port=self.__port__, key_filename=self.__keyfile__,
                                        timeout=self.__timeout__, look_for_keys=False)
        else:  # Username and password combo
            if self.__username__ is None or self.__password__ is None:
                raise paramiko.SSHException("You must enter a username and password or supply an SSH key")
            else:
                self.connection.connect(self.__host__, port=self.__port__, username=self.__username__,
                                        password=self.__password__, timeout=self.__timeout__, look_for_keys=False)
        # per https://github.com/paramiko/paramiko/issues/175
        self.connection.get_transport().window_size = 3 * 1024 * 1024


def _validate_hook_(hook):
    """Private method to take a pre or post hook and validate it!

    - **parameters** and **return types**::

        :param hook: Dictionary of {'func':<function>, 'args':[<args>], 'kwargs':{<dictionary>}}
        :return: Dictionary
    """
    if type(hook) is not dict:
        raise InvalidHook(str(hook) + " is not of type dict")
    hookkeys = hook.keys()
    if 'func' in hookkeys:
        if type(hook['func']) is not FunctionType:
            raise TypeError("'func' is not type FunctionType")
    if 'args' in hookkeys:
        if type(hook['args']) is list:
            pass
        elif type(hook['args']) is tuple:
            hook['args'] = list(hook['args'])
        else:
            hook['args'] = [hook['args']]
    else:
        hook['args'] = []
    if 'kwargs' in hookkeys:
        if type(hook['kwargs']) is not dict:
            raise TypeError("'kwargs' is not type dict")
    else:
        hook['kwargs'] = {}
    return hook


class ServerJob(object):
    """
    Custom class for holding all the info needed to run ssh commands or shell commands in subprocesses or threads

    - **parameters** and **return types**::

        :param fqdn: Fully qualified domain name or IP address
        :param cmds: List of commands to run (in the order you want them run)
        :param username: Username for SSH
        :param password: Password for SSH
        :param keyfile: Path to ssh key (can be used instead of password)
        :param debuglevel: 0 = off, 1 = some, 2 = more, 3 = all
        :param timeout: Tuple of timeouts (sshtimeout, cmdtimeout), if not specified both default to 30 seconds
        :param runlocal: Run job on localhost (skips ssh to localhost)
        :param prehook: Dictionary of {'func':<function>, 'args':[<args>], 'kwargs':{<dictionary>}}
        :param posthook: Dictionary of {'func':<function>, 'args':[<args>], 'kwargs':{<dictionary>}}
        :return: serverJob Object

    - **properties**::
        :property cmdResults: List of results of each command in tuple form (cmd, stdout, stderr)
        :propery cmdStatus: List of states for each command ( None = initial state/cmd did not run, True = no stderr,
                            False = stderr)
        :property status: State of entire job (None = initial state/ssh failed, True = all cmd statuses is True,
                            False = one or more cmd statuses is False)
        :property prehook_return: Returned values from prehook method
        :property posthook_return: Returned values from posthook method
        :property combine_output: Combine stdout and stderr in cmdResults (default = False)
    """
    def __init__(self, fqdn, cmds, username=None, password=None, keyfile=None, debuglevel=0, timeout=(30, 30),
                 runlocal=False, prehook=None, posthook=None):
        if type(cmds) in (list, tuple):
            self.cmds = cmds
        else:
            self.cmds = [cmds]
        self.cmdResults = []
        self.cmdStatus = []
        self.username = username
        self.password = password
        self.key = keyfile
        self.status = None
        if type(timeout) in (tuple, list):
            if len(timeout) != 2:
                raise InvalidArgument('You must supply two timeouts if you pass a tuple or list')
            self.sshtimeout = timeout[0]
            self.cmdtimeout = timeout[1]
        else:
            self.sshtimeout = timeout
            self.cmdtimeout = timeout
        self.runlocal = runlocal
        self.name = fqdn
        self.prehook_return = None
        if prehook is not None:
            self.prehook = _validate_hook_(prehook)
        else:
            self.prehook = None
        self.posthook_return = None
        if posthook is not None:
            self.posthook = _validate_hook_(posthook)
        else:
            self.posthook = None
        self.combine_output = False
        try:
            if int(debuglevel) <= 3:
                self.debuglevel = debuglevel
            else:
                raise TypeError("Debug level must be an integer between 0 and 3")
        except Exception:
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

        - **parameters** and **return types**::

            :return: serverJob.status
        """
        if self.debuglevel >= 1:
            print("Running serverJob: " + self.name)
        # Run prehook if it is defined
        if self.prehook is not None:
            if self.debuglevel >= 2:
                print("Running prehook")
            self.prehook['args'].append(self)
            self.prehook_return = self.prehook['func'](*self.prehook['args'], **self.prehook['kwargs'])
            self.prehook['args'].remove(self)
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
            except Exception, errorMsg:
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
            self.posthook['args'].append(self)
            self.posthook_return = self.posthook['func'](*self.posthook['args'], **self.posthook['kwargs'])
            self.posthook['args'].remove(self)
        if self.debuglevel >= 1:
            print("Finished running serverJob: " + self.name)
        return self.status

    def print_results(self, printname=False):
        """Prints the command run and its output

        - **parameters** and **return types**::

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
