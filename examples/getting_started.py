#!/usr/bin/env python
# coding=utf-8
"""Examples for sshreader module
"""
from __future__ import print_function
import sshreader

hosts = ['host1.example.com', 'host2.example.com']

# Create a list of ServerJob objects with commands to run on each server
serverjobs = list()
for host in hosts:
    # Create the ServerJob object with the shell commands you want to run
    serverjobs.append(sshreader.ServerJob(host, ['uname -a', 'uptime'], username='jdoe', password='password1234'))

# sshread the list of ServerJobs as quickly as possible!
# setting pcount and tcount to 0 will let sshreader figure out the number of processes and threads to spawn for best
# results.
results = sshreader.sshread(serverjobs, pcount=0, tcount=0, progress_bar=True)

# Output the results from each job
for result in results:
    result.print_results()

# You can also use sshreader to work with ssh connections without threading/multiprocessing
with sshreader.SSH('192.168.1.1', username='jdoe', password='password1234') as s:
    print(s.ssh_command('uname -a'))

# Or you can run shell commands on the localhost
print(sshreader.shell_command('uname -a'))

