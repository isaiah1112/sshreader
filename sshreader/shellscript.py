#!/usr/bin/env python
# coding=utf-8
"""A helper for running shell scripts
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
from subprocess import Popen, PIPE, STDOUT
from pkg_resources import get_distribution

__author__ = 'Jesse Almanrode (jesse@almanrode.com)'
__version__ = get_distribution('sshreader').version


def do_shell_script(command, combine=False):
    """Run a specified command in the shell on localhost and return the output

    - **parameters** and **return types**::

        :param command: String containing the shell script to run
        :param combine: Combine stderr and stdout in output
        :return: Tuple of (command,stdout,stderr) or (command,output)
    """
    if combine:
        pipeout = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT).stdout
        stdout = pipeout.read()
        return command, stdout.strip()
    else:
        pipeout = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = pipeout.communicate()
        return command, stdout.strip(), stderr.strip()
