#!/usr/bin/env python
# coding=utf-8
""" Integration and Unit tests for sshreader Python Package
"""
import json
import os
import sys
import unittest
import warnings

__author__ = 'Jesse Almanrode (jesse@almanrode.com)'
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
import sshreader

global ssh_data
try:
    # If you want to test locally simply create a test_params.json file like the dictionary below
    params_file = open(project_root + '/tests/test_params.json')
    ssh_data = json.load(params_file)
except IOError:
    # Defaults for testing with Docker!
    ssh_data = {"host_fqdn": "127.0.0.1", "ssh_user": "sshreader", "ssh_password": "sunshine",
                "ssh_key_path": project_root + "/tests/keys/id_rsa"}


class TestShellScript(unittest.TestCase):
    """ Test Cases for the shell script portion of SSH module
    """

    def test_shell_command(self):
        """ Test shell_command method
        """
        result = sshreader.shell_command('echo "foo"')
        self.assertEqual(result.return_code, 0)
        self.assertIn('foo', result.stdout)
        self.assertEqual(len(result.stderr), 0)
        pass

    def test_shell_command_combined(self):
        """ Test combining stdout and stderr of shell_command method
        """
        result = sshreader.shell_command('echo "foo"; echo "bar" 1>&2', combine=True)
        self.assertEqual(result.return_code, 0)
        self.assertIn('foo', result.stdout)
        self.assertIn('bar', result.stdout)
        self.assertEqual(result.stderr, None)
        pass

    def test_shell_command_stderr(self):
        """ Test stderr of shell_command method
        """
        result = sshreader.shell_command('echo "bar" 1>&2')
        self.assertEqual(result.return_code, 0)
        self.assertEqual(len(result.stdout), 0)
        self.assertIn('bar', result.stderr)
        pass

    def test_decode_bytes(self):
        """ Test to ensure that result is a unicode string type
        """
        result = sshreader.shell_command('uname -a', decodebytes=True)
        self.assertEqual(result.return_code, 0)
        self.assertIsInstance(result.stdout, str)
        pass


class TestSSH(unittest.TestCase):
    """ Test cases for the SSH class
    """

    def setUp(self):
        """ Setup SSH connection
        :return: Connection state conn.is_alive()
        """
        global ssh_data
        self.conn = sshreader.SSH(ssh_data['host_fqdn'], username=ssh_data['ssh_user'],
                                  password=ssh_data['ssh_password'], connect=False)
        return self.conn.alive()

    def test_password(self):
        """ Test an SSH connection using a password
        """
        self.conn.connect()
        self.conn.alive()
        self.assertTrue(self.conn.alive(), msg='ssh connection using password failed to: ' + ssh_data['host_fqdn'])
        self.conn.close()
        pass

    def test_keyfile(self):
        """ Test an SSH connection using an ssh key
        """
        global ssh_data
        conn = sshreader.SSH(ssh_data['host_fqdn'], username=ssh_data['ssh_user'], keyfile=ssh_data['ssh_key_path'])
        self.assertTrue(conn.alive(), msg='ssh connection using password failed to: ' + ssh_data['host_fqdn'])
        pass

    def test_reconnect(self):
        """ Test re-opening an SSH connection
        """
        self.assertFalse(self.conn.alive())
        self.conn.reconnect()
        self.assertTrue(self.conn.alive())
        pass

    def test_command(self):
        """ Test an ssh_command
        """
        self.assertFalse(self.conn.alive())
        self.conn.connect()
        result = self.conn.ssh_command('echo foo')
        self.assertEqual(result.return_code, 0)
        self.assertIn('foo', result.stdout)
        self.assertEqual(len(result.stderr), 0)
        pass

    def test_command_stderr(self):
        """ Test an ssh_command
        """
        self.assertFalse(self.conn.alive())
        self.conn.connect()
        result = self.conn.ssh_command('echo bar 1>&2')
        self.assertEqual(result.return_code, 0)
        self.assertEqual(len(result.stdout), 0)
        self.assertIn('bar', result.stderr)
        pass

    def test_combine_output(self):
        """ Test combining stdout and stderr of ssh_command
        """
        self.assertFalse(self.conn.alive())
        self.conn.connect()
        result = self.conn.ssh_command('echo foo; echo bar 1>&2;', combine=True)
        self.assertIsInstance(result, tuple)
        self.assertEqual(result.return_code, 0)
        self.assertIn('foo', result.stdout)
        self.assertIn('bar', result.stdout)
        pass

    def test_cmd_timeout(self):
        """ Test handling of cmd timeout via SSH
        """
        if self.conn.alive() is False:
            self.conn.connect()
        self.assertTrue(self.conn.alive())
        result = self.conn.ssh_command('sleep 5', timeout=2)
        self.assertEqual(result.return_code, 124)
        self.assertEqual(len(result.stdout), 0)
        self.assertIn('command timed out', result.stderr)
        pass


def my_hook(*args):
    """ Function for testing hook
    :param args: Args should be ('pre|post', sshreader.ServerJob)
    :return:
    """
    args = list(args)
    if len(args) == 1:
        if args[0] in ('pre', 'post') and isinstance(args.pop(), sshreader.ServerJob):
            return True
        else:
            return False
    else:
        if args[0] in ('pre', 'post'):
            return True
        else:
            return False


class TestSshreader(unittest.TestCase):
    """ Test cases for the sshreader module
    """

    @staticmethod
    def configure_serverjob_list(size):
        """ Configure a list of serverjob objects to sshread (including pre and post hooks) and local commands
        :return: List
        """
        global ssh_data
        pre = sshreader.Hook(my_hook, args=['pre'])
        post = sshreader.Hook(my_hook, args=['post'])
        jobs = list()
        for x in range(size):
            x = sshreader.ServerJob(ssh_data['host_fqdn'], ['sleep 1', 'echo done'], prehook=pre, posthook=post,
                                    username=ssh_data['ssh_user'], password=ssh_data['ssh_password'])
            jobs.append(x)
        for x in range(size):
            jobs.append(sshreader.ServerJob('local-' + str(x), ['sleep 1', 'echo done'], runlocal=True))
        return jobs

    def test_Hook_creation(self):
        """ Test valid hook creation
        """
        myhook = sshreader.Hook(my_hook, args=['pre'])
        self.assertIsInstance(myhook, sshreader.Hook)
        pass

    def test_ServerJob(self):
        """ Test valid ServerJob creation
        """
        global ssh_data
        job = sshreader.ServerJob(ssh_data['host_fqdn'], 'echo foo',
                                  username=ssh_data['ssh_user'], password=ssh_data['ssh_password'])
        self.assertIsInstance(job, sshreader.ServerJob)
        pass

    def test_ServerJob_with_hooks(self):
        """ Test ServerJob with hooks
        """
        global ssh_data
        pre = sshreader.Hook(my_hook, args=['pre'])
        post = sshreader.Hook(my_hook, args=['post'])
        job = sshreader.ServerJob(ssh_data['host_fqdn'], 'echo foo', prehook=pre, posthook=post,
                                  username=ssh_data['ssh_user'], password=ssh_data['ssh_password'])
        self.assertIsInstance(job, sshreader.ServerJob)
        pass

    def test_sshread_threads(self):
        """ Test sshread method using threads
        """
        jobs = self.configure_serverjob_list(1)
        result = sshreader.sshread(jobs, tcount=0)
        for x in result:
            self.assertEqual(x.status, 0, msg=x.results)
        pass

    def test_sshread_processes(self):
        """ Test sshread method using processes
        """
        jobs = self.configure_serverjob_list(1)
        result = sshreader.sshread(jobs, pcount=0)
        for x in result:
            self.assertEqual(x.status, 0, msg=x.results)
        pass

    def test_sshread(self):
        """ Test sshread method using threads and processes
        """
        jobs = self.configure_serverjob_list(1)
        result = sshreader.sshread(jobs, pcount=0, tcount=0)
        for x in result:
            self.assertEqual(x.status, 0, msg=x.results)
        pass

    def test_cpulimits(self):
        """ Ensure the cpulimit methods
        """
        self.assertIsInstance(sshreader.utils.cpusoftlimit(), int)
        self.assertIsInstance(sshreader.utils.cpuhardlimit(), int)
        pass

    def test_threadlimits(self):
        """ Ensure the threadlimit method
        """
        self.assertIsInstance(sshreader.utils.threadlimit(), int)
        pass


if __name__ == '__main__':
    with warnings.catch_warnings(record=True):
        unittest.main()
