import threading

from sshreader.utils import ServerJob, sshread, _sub_process_


def test_sshread_progress_bar(monkeypatch):
    # Fake Value used as item_counter
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

    # Patch ProgressBar and mpctx.Value/Lock
    import sshreader.utils as utils
    monkeypatch.setattr(utils, 'ProgressBar', FakeBar)
    monkeypatch.setattr(utils.mpctx, 'Value', lambda t, v: FakeValue(v))

    j1 = ServerJob('p1', 'echo one', run_local=True)
    j2 = ServerJob('p2', 'echo two', run_local=True)
    # Avoid touching mpctx.Lock to not interfere with multiprocessing internals
    res = sshread([j1, j2], pcount=None, tcount=2, progress_bar=True, print_lock=False)
    assert isinstance(res, list)
    assert updates['count'] >= 1
    assert updates['finished'] is True


def test__sub_process_thread_branch():
    # Use simple in-process queues
    from queue import Queue

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
    # Put two jobs
    j1 = ServerJob('s1', 'echo a', run_local=True)
    j2 = ServerJob('s2', 'echo b', run_local=True)
    tq.put(j1)
    tq.put(j2)

    # Run the subprocess worker with thread_count > 0
    _sub_process_(tq, rq, None, thread_count=2, progress_bar=False)

    # Both jobs should be processed and available in result queue
    out1 = rq.get()
    out2 = rq.get()
    names = {out1.name, out2.name}
    assert {'s1', 's2'} == names
