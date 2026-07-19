import time

from sshreader.utils import ServerJob, sshread, mpctx


def test_sshread_process_mode_monkeypatched(monkeypatch):
    # Fake Process that runs the target synchronously
    class FakeProcess:
        def __init__(self, target=None, args=(), daemon=False):
            self._target = target
            self._args = args

        def start(self):
            # run synchronously in test process
            self._target(*self._args)

        def is_alive(self):
            return False

        def join(self, timeout=None):
            return None

        def close(self):
            return None

    # Patch mpctx.Process and allow_connection_pickling
    monkeypatch.setattr(mpctx, 'Process', FakeProcess)
    monkeypatch.setattr(mpctx, 'allow_connection_pickling', lambda: None)

    # Two local ServerJobs (run_local True so they execute shell_command)
    j1 = ServerJob('h1', 'echo one', run_local=True)
    j2 = ServerJob('h2', 'echo two', run_local=True)

    results = sshread([j1, j2], pcount=1, tcount=0, progress_bar=False, print_lock=False)
    assert isinstance(results, list)
    assert len(results) == 2
