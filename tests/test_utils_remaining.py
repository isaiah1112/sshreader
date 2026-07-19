from queue import Queue


def test_echo_with_lockobj(capsys):
    import sshreader.utils as utils

    class DummyLock:
        def __init__(self):
            self.entered = False

        def __enter__(self):
            self.entered = True

        def __exit__(self, exc_type, exc, tb):
            return False

    lock = DummyLock()
    # set the global lockobj
    utils.lockobj = lock
    utils.echo('y', end='')
    out = capsys.readouterr().out
    assert out == 'y'
    # cleanup
    utils.lockobj = None


def test_sshread_pcount_zero_and_negative(monkeypatch):
    import sshreader.utils as utils
    from sshreader.utils import ServerJob

    # Fake Process that runs target synchronously
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
    # Force cpu_count for cpu_limit
    monkeypatch.setattr(utils.mpctx, 'cpu_count', lambda: 2)

    jobs = [ServerJob(f'h{i}', 'echo hi', run_local=True) for i in range(3)]

    res0 = utils.sshread(jobs, pcount=0, tcount=0, progress_bar=False, print_lock=False)
    assert isinstance(res0, list)
    assert len(res0) == 3

    resneg = utils.sshread(jobs, pcount=-1, tcount=0, progress_bar=False, print_lock=False)
    assert isinstance(resneg, list)
    assert len(resneg) == 3


def test__sub_process_non_thread_path():
    from sshreader.utils import _sub_process_
    from sshreader.utils import ServerJob

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

    _sub_process_(tq, rq, None, thread_count=0, progress_bar=False)

    out1 = rq.get()
    out2 = rq.get()
    assert {out1.name, out2.name} == {'s1', 's2'}
