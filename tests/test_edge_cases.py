import os

import logging
import paramiko
import pytest

import sshreader
from sshreader.utils import ServerJob, Hook, shell_command, cpu_limit
from sshreader.ssh import SSH


def test_serverjob_timeout_tuple_length():
    with pytest.raises(ValueError):
        ServerJob('h', 'cmd', timeout=(1, 2, 3))


def test_serverjob_prehook_typeerror():
    with pytest.raises(TypeError):
        ServerJob('h', 'cmd', pre_hook=object(), run_local=True)


def test_serverjob_getitem_and_str():
    job = ServerJob('h', ['echo hi'], run_local=True)
    s = str(job)
    assert 'name' in s
    assert job['name'] == 'h'


def test_hook_args_kwargs_merge():
    def target(a, b=0, c=0):
        return a + b + c

    h = Hook(target, args=[1], kwargs={'b': 2})
    # Call without an extra positional to avoid duplicate 'b' values
    res = h.run(c=4)
    assert res == 1 + 2 + 4


def test_shell_command_decode_false():
    res = shell_command('echo ok', decode_bytes=False)
    assert isinstance(res.stdout, (bytes, str))


def test_cpu_limit_warning(caplog, monkeypatch):
    caplog.set_level(logging.WARNING)
    monkeypatch.setattr('sshreader.utils.mpctx.cpu_count', lambda: 4)
    # factor > 2 should emit a warning
    cpu_limit(3)
    assert any('greater than 2' in r.message for r in caplog.records)


def test_ssh_command_timeout_returns_124(monkeypatch):
    # Prepare SSH instance with fake client that raises TimeoutError
    class FakeAgent:
        def get_keys(self):
            return ['k']

    monkeypatch.setattr(paramiko, 'Agent', lambda: FakeAgent())

    class TimeoutSSHClient:
        def __init__(self):
            pass

        def set_missing_host_key_policy(self, p):
            pass

        def exec_command(self, command, timeout=None, get_pty=False):
            raise TimeoutError()

        def get_transport(self):
            class T:
                def is_alive(self):
                    return True

            return T()

    monkeypatch.setattr(paramiko, 'SSHClient', TimeoutSSHClient)
    s = SSH('h', 'u', password='p', connect=False)
    s._connection = TimeoutSSHClient()
    res = s.ssh_command('cmd', combine=False)
    assert res.return_code == 124


def test_ssh_connect_raises_if_already_alive(monkeypatch):
    class FakeAgent:
        def get_keys(self):
            return ['k']

    monkeypatch.setattr(paramiko, 'Agent', lambda: FakeAgent())
    s = SSH('h', 'u', password='p', connect=False)
    # force __alive to return True
    monkeypatch.setattr(s, '_SSH__alive', lambda: True)
    with pytest.raises(paramiko.SSHException):
        s.connect()


def test__sub_thread_worker(monkeypatch, tmp_path):
    # Test the private thread worker using a local ServerJob
    from sshreader import utils

    job = ServerJob('t1', 'echo hi', run_local=True)
    # Use simple in-process queues to avoid multiprocessing timing/pickling
    from queue import Queue

    class SimpleQ:
        def __init__(self):
            self.q = Queue()

        def empty(self):
            return self.q.empty()

        def get(self, timeout=None):
            return self.q.get(timeout=timeout) if timeout else self.q.get()

        def put(self, item):
            return self.q.put(item)

    tq = SimpleQ()
    rq = SimpleQ()
    tq.put(job)
    # Call the worker directly
    utils._sub_thread_(tq, rq, None, False)
    # Ensure the job was processed and put into the result queue
    got = rq.get(timeout=1)
    assert getattr(got, 'name', None) == 't1'
