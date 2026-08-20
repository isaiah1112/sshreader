import logging
from queue import Empty, Queue

import pytest

import sshreader.utils as utils
from sshreader.customtypes import Command
from sshreader.utils import ServerJob, Hook, shell_command, cpu_limit


def test_shell_command_basic():
    result = utils.shell_command('echo hello', combine=False)
    assert isinstance(result, Command)
    assert 'hello' in result.stdout
    assert result.return_code == 0


def test_shell_command_combine_and_decode():
    cmd = "python -c \"import sys; sys.stdout.write('out'); sys.stderr.write('err'); sys.exit(3)\""
    result = utils.shell_command(cmd, combine=True)
    assert result.stderr is None
    assert 'out' in result.stdout
    assert result.return_code == 3


def test_shell_command_decode_false():
    res = shell_command('echo ok', decode_bytes=False)
    assert isinstance(res.stdout, (bytes, str))


def test_hook_run_and_str():
    def target(a, b=0):
        return a + b

    h = utils.Hook(target, args=[1], kwargs={'b': 2})
    res = h.run()
    assert res == 3
    s = str(h)
    assert 'target' in s


def test_hook_args_kwargs_merge():
    def target(a, b=0, c=0):
        return a + b + c

    h = Hook(target, args=[1], kwargs={'b': 2})
    res = h.run(c=4)
    assert res == 1 + 2 + 4


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


def test_cpu_limit_monkeypatch(monkeypatch):
    monkeypatch.setattr(utils.mpctx, 'cpu_count', lambda: 4)
    assert utils.cpu_limit(1) == 4
    assert utils.cpu_limit(2) == 8


def test_cpu_limit_warning(caplog, monkeypatch):
    caplog.set_level(logging.WARNING)
    monkeypatch.setattr('sshreader.utils.mpctx.cpu_count', lambda: 4)
    cpu_limit(3)
    assert any('greater than 2' in r.message for r in caplog.records)


def test_echo_prints(capsys):
    utils.echo('x', end='')
    out = capsys.readouterr().out
    assert out == 'x'


def test_echo_with_lockobj(capsys):
    class DummyLock:
        def __init__(self):
            self.entered = False

        def __enter__(self):
            self.entered = True

        def __exit__(self, exc_type, exc, tb):
            return False

    lock = DummyLock()
    utils.lockobj = lock
    utils.echo('y', end='')
    out = capsys.readouterr().out
    assert out == 'y'
    utils.lockobj = None


def test_sshread_threads():
    j1 = utils.ServerJob('l1', 'echo one', run_local=True)
    j2 = utils.ServerJob('l2', 'echo two', run_local=True)
    results = utils.sshread([j1, j2], tcount=2, pcount=None, progress_bar=False, print_lock=False)
    assert isinstance(results, list)
    assert len(results) == 2


def test__sub_thread_worker(monkeypatch, tmp_path):
    job = ServerJob('t1', 'echo hi', run_local=True)

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
    utils._sub_thread_(tq, rq, None, False)
    got = rq.get(timeout=1)
    assert getattr(got, 'name', None) == 't1'


def test_sshread_process_mode_monkeypatched(monkeypatch):
    class FakeProcess:
        def __init__(self, target=None, args=(), daemon=False):
            self._target = target
            self._args = args

        def start(self):
            self._target(*self._args)

        def is_alive(self):
            return False

        def join(self, timeout=None):
            return None

        def close(self):
            return None

    monkeypatch.setattr(utils.mpctx, 'Process', FakeProcess)
    monkeypatch.setattr(utils.mpctx, 'allow_connection_pickling', lambda: None)

    j1 = ServerJob('h1', 'echo one', run_local=True)
    j2 = ServerJob('h2', 'echo two', run_local=True)
    results = utils.sshread([j1, j2], pcount=1, tcount=0, progress_bar=False, print_lock=False)
    assert isinstance(results, list)
    assert len(results) == 2


def test_sshread_pcount_zero_and_negative(monkeypatch):
    class FakeProcess:
        def __init__(self, target=None, args=(), daemon=False):
            self._target = target
            self._args = args

        def start(self):
            self._target(*self._args)

        def is_alive(self):
            return False

        def join(self, timeout=None):
            return None

        def close(self):
            return None

    monkeypatch.setattr(utils.mpctx, 'Process', FakeProcess)
    monkeypatch.setattr(utils.mpctx, 'allow_connection_pickling', lambda: None)
    monkeypatch.setattr(utils.mpctx, 'cpu_count', lambda: 2)

    jobs = [ServerJob(f'h{i}', 'echo hi', run_local=True) for i in range(3)]
    res0 = utils.sshread(jobs, pcount=0, tcount=0, progress_bar=False, print_lock=False)
    assert isinstance(res0, list)
    assert len(res0) == 3
    resneg = utils.sshread(jobs, pcount=-1, tcount=0, progress_bar=False, print_lock=False)
    assert isinstance(resneg, list)
    assert len(resneg) == 3


def test_sub_thread_handles_stale_empty_queue():
    class StaleEmptyQueue:
        def __init__(self, jobs):
            self._jobs = list(jobs)
            self._empty_calls = 0

        def empty(self):
            self._empty_calls += 1
            return self._empty_calls == 1

        def get(self, timeout=None):
            if not self._jobs:
                raise Empty()
            return self._jobs.pop(0)

    class ResultQueue:
        def __init__(self):
            self.items = []

        def put(self, item):
            self.items.append(item)

    job = ServerJob('h1', 'echo hi', run_local=True)
    tq = StaleEmptyQueue([job])
    rq = ResultQueue()
    utils._sub_thread_(tq, rq, None, False)
    assert len(rq.items) == 1


def test_sshread_progress_bar(monkeypatch):
    class FakeValue:
        def __init__(self, init=0):
            self.value = init

        def get_lock(self):
            class L:
                def __enter__(self):
                    return None

                def __exit__(self, exc_type, exc, tb):
                    return None

            return L()

    updates = {'count': 0, 'finished': False}

    class FakeBar:
        def __init__(self, max_value=None):
            self.max = max_value

        def update(self, v):
            updates['count'] += 1

        def finish(self):
            updates['finished'] = True

    monkeypatch.setattr(utils, 'ProgressBar', FakeBar)
    monkeypatch.setattr(utils.mpctx, 'Value', lambda t, v: FakeValue(v))

    j1 = ServerJob('p1', 'echo one', run_local=True)
    j2 = ServerJob('p2', 'echo two', run_local=True)
    res = utils.sshread([j1, j2], pcount=None, tcount=2, progress_bar=True, print_lock=False)
    assert isinstance(res, list)
    assert updates['count'] >= 1
    assert updates['finished'] is True


def test__sub_process_thread_branch():
    class SimpleQ:
        def __init__(self):
            self.q = Queue()

        def empty(self):
            return self.q.empty()

        def get(self):
            return self.q.get()

        def put(self, item):
            return self.q.put(item)

    tq = SimpleQ()
    rq = SimpleQ()
    j1 = ServerJob('s1', 'echo a', run_local=True)
    j2 = ServerJob('s2', 'echo b', run_local=True)
    tq.put(j1)
    tq.put(j2)
    utils._sub_process_(tq, rq, None, thread_count=2, progress_bar=False)
    out1 = rq.get()
    out2 = rq.get()
    names = {out1.name, out2.name}
    assert {'s1', 's2'} == names


def test__sub_process_non_thread_path():
    class SimpleQ:
        def __init__(self):
            self.q = Queue()

        def empty(self):
            return self.q.empty()

        def get(self):
            return self.q.get()

        def put(self, item):
            return self.q.put(item)

    tq = SimpleQ()
    rq = SimpleQ()
    tq.put(ServerJob('s1', 'echo a', run_local=True))
    tq.put(ServerJob('s2', 'echo b', run_local=True))
    utils._sub_process_(tq, rq, None, thread_count=0, progress_bar=False)
    out1 = rq.get()
    out2 = rq.get()
    assert {out1.name, out2.name} == {'s1', 's2'}
