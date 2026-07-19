import time

import pytest

import sshreader.utils as utils
from sshreader.customtypes import Command


def test_shell_command_basic():
    result = utils.shell_command('echo hello', combine=False)
    assert isinstance(result, Command)
    assert 'hello' in result.stdout
    assert result.return_code == 0


def test_shell_command_combine_and_decode():
    # create command that writes to stderr and exits with code 3
    cmd = "python -c \"import sys; sys.stdout.write('out'); sys.stderr.write('err'); sys.exit(3)\""
    result = utils.shell_command(cmd, combine=True)
    assert result.stderr is None
    assert 'out' in result.stdout
    assert result.return_code == 3


def test_hook_run_and_str():
    def target(a, b=0):
        return a + b

    h = utils.Hook(target, args=[1], kwargs={'b': 2})
    res = h.run()
    # target called with args [1]
    assert res == 3
    s = str(h)
    assert 'target' in s


def test_serverjob_run_local_and_hooks():
    pre_called = []
    post_called = []

    def pre(job):
        pre_called.append(job.name)

    def post(job):
        post_called.append(job.name)

    prehook = utils.Hook(pre)
    posthook = utils.Hook(post)
    job = utils.ServerJob('localhost', ['echo a', 'bash -c "exit 2"'], run_local=True,
                          pre_hook=prehook, post_hook=posthook)
    status = job.run()
    assert status == 2
    assert len(job.results) == 2
    assert pre_called == ['localhost']
    assert post_called == ['localhost']


def test_cpu_limit_monkeypatch(monkeypatch):
    monkeypatch.setattr(utils.mpctx, 'cpu_count', lambda: 4)
    assert utils.cpu_limit(1) == 4
    assert utils.cpu_limit(2) == 8


def test_echo_prints(capsys):
    utils.echo('x', end='')
    out = capsys.readouterr().out
    assert out == 'x'


def test_sshread_threads():
    # Two simple local ServerJobs
    j1 = utils.ServerJob('l1', 'echo one', run_local=True)
    j2 = utils.ServerJob('l2', 'echo two', run_local=True)
    results = utils.sshread([j1, j2], tcount=2, pcount=None, progress_bar=False, print_lock=False)
    assert isinstance(results, list)
    assert len(results) == 2
    assert all(hasattr(r, 'results') for r in results)