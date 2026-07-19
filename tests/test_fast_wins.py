import paramiko

from sshreader.ssh import SSH
from sshreader.utils import ServerJob


def test_connect_disabled_algorithms(monkeypatch):
    # Ensure Agent has keys so constructor doesn't reject
    monkeypatch.setattr(paramiko, 'Agent', lambda: type('A', (), {'get_keys': lambda self: ['k']})())

    captured = {}

    class FakeSSHClient:
        def __init__(self):
            pass

        def set_missing_host_key_policy(self, p):
            pass

        def get_transport(self):
            return None

        def connect(self, *args, **kwargs):
            captured.update(kwargs)

    monkeypatch.setattr(paramiko, 'SSHClient', FakeSSHClient)

    s = SSH('h', 'u', password='p', keyfile='/tmp/fake', connect=False, rsa_sha2=False)
    s._connection = FakeSSHClient()
    s.connect()
    assert 'disabled_algorithms' in captured


def test_serverjob_connect_failure(monkeypatch):
    # Fake SSH that raises on connect
    class FakeSSH:
        def __init__(self, host, username, password=None, keyfile=None, port=22, connect=False, rsa_sha2=True):
            pass

        def connect(self, timeout=0.5):
            raise Exception('conn fail')

    monkeypatch.setattr('sshreader.utils.SSH', FakeSSH)

    job = ServerJob('h', 'echo hi', username='u', password='p', run_local=False)
    status = job.run()
    assert status == 255
    assert isinstance(job.results[0], str)
    assert 'conn fail' in job.results[0]


def test_serverjob_command_exception(monkeypatch):
    # Fake SSH where connect works but ssh_command raises
    class FakeSSH2:
        def __init__(self, host, username, password=None, keyfile=None, port=22, connect=False, rsa_sha2=True):
            pass

        def connect(self, timeout=0.5):
            return True

        def ssh_command(self, cmd, timeout=0.5, combine=False):
            raise RuntimeError('cmd fail')

        def close(self):
            return None

    monkeypatch.setattr('sshreader.utils.SSH', FakeSSH2)

    job = ServerJob('h', ['echo a'], username='u', password='p', run_local=False)
    status = job.run()
    # The per-command exception should be converted into a Command with rc 54
    assert any(getattr(r, 'return_code', None) == 54 for r in job.results)
    assert any('cmd fail' in (getattr(r, 'stderr', '') or str(r)) for r in job.results)
