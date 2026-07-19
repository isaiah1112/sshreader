import os

import paramiko
import pytest

from sshreader.ssh import envvars, SSH


def test_envvars_with_ssh_keys_and_agent(monkeypatch, tmp_path):
    # Create fake HOME with .ssh containing keys
    home = tmp_path
    sshdir = home / '.ssh'
    sshdir.mkdir()
    (sshdir / 'id_rsa').write_text('priv')
    (sshdir / 'id_dsa').write_text('priv')
    (sshdir / 'id_ecdsa').write_text('priv')

    monkeypatch.setenv('HOME', str(home))
    monkeypatch.setattr('sshreader.ssh.getuser', lambda: 'tester')

    class FakeAgent:
        def get_keys(self):
            return ['agentkey']

    monkeypatch.setattr(paramiko, 'Agent', lambda: FakeAgent())

    e = envvars()
    assert e.username == 'tester'
    assert e.rsa_key is not None
    assert e.dsa_key is not None
    assert e.ecdsa_key is not None
    assert e.agent_keys == ['agentkey']


def test_envvars_no_ssh_dir_and_no_agent(monkeypatch, tmp_path):
    monkeypatch.setenv('HOME', str(tmp_path))
    # getuser raises => fallback to home last path part
    monkeypatch.setattr('sshreader.ssh.getuser', lambda: (_ for _ in ()).throw(OSError()))
    class FakeAgent:
        def get_keys(self):
            return []

    monkeypatch.setattr(paramiko, 'Agent', lambda: FakeAgent())
    e = envvars()
    assert e.username == str(tmp_path).split('/')[-1]
    assert e.rsa_key is None
    assert e.agent_keys == []


def test_ssh_init_keyfile_type_error(monkeypatch):
    # Ensure Agent reports no keys so keyfile branch exercised
    class FakeAgent:
        def get_keys(self):
            return []

    monkeypatch.setattr(paramiko, 'Agent', lambda: FakeAgent())
    with pytest.raises(TypeError):
        SSH('host', 'user', keyfile=123, connect=False)


def test_ssh_command_and_sftp_and_alive(monkeypatch):
    # Provide a working Agent
    class FakeAgent:
        def get_keys(self):
            return ['k']

    monkeypatch.setattr(paramiko, 'Agent', lambda: FakeAgent())

    # Fake transport and channel
    class FakeChannel:
        def recv_exit_status(self):
            return 0

    class FakeFile:
        def __init__(self, data):
            self._b = data.encode()
        def read(self):
            return self._b

        # Provide a channel with recv_exit_status used by ssh_command
        @property
        def channel(self):
            class C:
                def recv_exit_status(self):
                    return 0

            return C()

    class FakeTransport:
        def is_alive(self):
            return True

    class FakeSFTP:
        def __init__(self):
            self.put_called = False

        def put(self, src, dst):
            self.put_called = True
            return True

        def get(self, src, dst):
            # simulate copying
            open(dst, 'w').write('ok')

        def close(self):
            return None

    class FakeSSHClient:
        def __init__(self):
            self._transport = FakeTransport()

        def set_missing_host_key_policy(self, p):
            pass

        def exec_command(self, command, timeout=None, get_pty=False):
            return (None, FakeFile('out\n'), FakeFile('err\n'))

        def get_transport(self):
            return self._transport

        def close(self):
            self._transport = None

        def connect(self, *args, **kwargs):
            # simulate establishing transport
            self._transport = FakeTransport()

    # Patch the SSHClient class used inside SSH
    monkeypatch.setattr(paramiko, 'SSHClient', FakeSSHClient)
    # Patch SFTPClient.from_transport
    monkeypatch.setattr(paramiko.SFTPClient, 'from_transport', staticmethod(lambda t: FakeSFTP()))

    s = SSH('host', 'user', password='pw', connect=False)
    # attach our fake client instance if constructor created another
    s._connection = FakeSSHClient()

    # alive should return True
    assert s.alive() is True

    # ssh_command normal
    res = s.ssh_command('echo hi', timeout=1, combine=False)
    assert res.return_code == 0
    assert 'out' in res.stdout

    # combine True returns stdout and stderr None
    res2 = s.ssh_command('echo hi', timeout=1, combine=True)
    assert res2.stderr is None

    # sftp put/get
    tmp_src = 'tests/test_ssh_tmp.txt'
    with open(tmp_src, 'w') as f:
        f.write('x')
    put_res = s.sftp_put(tmp_src, '/tmp/dst')
    assert put_res is True
    # get
    dst_local = 'tests/test_ssh_tmp_get.txt'
    s.sftp_get('/tmp/src', dst_local)
    assert os.path.exists(dst_local)
    os.remove(tmp_src)
    os.remove(dst_local)


def test_alive_raises_when_transport_dead(monkeypatch):
    class FakeAgent:
        def get_keys(self):
            return ['k']

    monkeypatch.setattr(paramiko, 'Agent', lambda: FakeAgent())

    class DeadTransport:
        def is_alive(self):
            return False

    class FakeSSHClient:
        def __init__(self):
            self._transport = DeadTransport()

        def set_missing_host_key_policy(self, p):
            pass

        def get_transport(self):
            return self._transport

    monkeypatch.setattr(paramiko, 'SSHClient', FakeSSHClient)
    s = SSH('h', 'u', password='p', connect=False)
    s._connection = FakeSSHClient()
    with pytest.raises(paramiko.SSHException):
        s.alive()
