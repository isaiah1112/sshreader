import os

import paramiko
import pytest

from sshreader.ssh import envvars, SSH


def test_envvars_with_ssh_keys_and_agent(monkeypatch, tmp_path):
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
    class FakeAgent:
        def get_keys(self):
            return []

    monkeypatch.setattr(paramiko, 'Agent', lambda: FakeAgent())
    with pytest.raises(TypeError):
        SSH('host', 'user', keyfile=123, connect=False)


def test_ssh_command_and_sftp_and_alive(monkeypatch):
    class FakeAgent:
        def get_keys(self):
            return ['k']

    monkeypatch.setattr(paramiko, 'Agent', lambda: FakeAgent())

    class FakeFile:
        def __init__(self, data):
            self._b = data.encode()

        def read(self):
            return self._b

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
            self._transport = FakeTransport()

    monkeypatch.setattr(paramiko, 'SSHClient', FakeSSHClient)
    monkeypatch.setattr(paramiko.SFTPClient, 'from_transport', staticmethod(lambda t: FakeSFTP()))

    s = SSH('host', 'user', password='pw', connect=False)
    s._connection = FakeSSHClient()

    assert s.alive() is True
    res = s.ssh_command('echo hi', timeout=1, combine=False)
    assert res.return_code == 0
    assert 'out' in res.stdout
    res2 = s.ssh_command('echo hi', timeout=1, combine=True)
    assert res2.stderr is None

    tmp_src = 'tests/test_ssh_tmp.txt'
    with open(tmp_src, 'w') as f:
        f.write('x')
    put_res = s.sftp_put(tmp_src, '/tmp/dst')
    assert put_res is True
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


def test_connect_disabled_algorithms(monkeypatch):
    monkeypatch.setattr(paramiko, 'Agent', lambda: type('A', (), {'get_keys': lambda self: ['k']})())

    captured = {}

    class FakeSSHClient2:
        def __init__(self):
            pass

        def set_missing_host_key_policy(self, p):
            pass

        def get_transport(self):
            return None

        def connect(self, *args, **kwargs):
            captured.update(kwargs)

    monkeypatch.setattr(paramiko, 'SSHClient', FakeSSHClient2)

    s = SSH('h', 'u', password='p', keyfile='/tmp/fake', connect=False, rsa_sha2=False)
    s._connection = FakeSSHClient2()
    s.connect()
    assert 'disabled_algorithms' in captured


def test_ssh_command_timeout_branches(monkeypatch):
    monkeypatch.setattr(paramiko, 'Agent', lambda: type('A', (), {'get_keys': lambda self: ['k']})())

    class TimeoutClient:
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

    monkeypatch.setattr(paramiko, 'SSHClient', TimeoutClient)
    s = SSH('h', 'u', password='p', connect=False)
    s._connection = TimeoutClient()
    res = s.ssh_command('cmd', combine=False)
    assert res.return_code == 124
    assert 'command timed out' in (res.stderr or '')
    res2 = s.ssh_command('cmd', combine=True)
    assert res2.return_code == 124
    assert 'command timed out' in (res2.stdout or '')


def test_sftp_methods_raise_when_not_alive(monkeypatch):
    monkeypatch.setattr(paramiko, 'Agent', lambda: type('A', (), {'get_keys': lambda self: ['k']})())

    class DeadClient:
        def __init__(self):
            pass

        def set_missing_host_key_policy(self, p):
            pass

        def get_transport(self):
            return None

    monkeypatch.setattr(paramiko, 'SSHClient', DeadClient)
    s = SSH('h', 'u', password='p', connect=False)
    s._connection = DeadClient()
    from paramiko import SSHException
    with pytest.raises(SSHException):
        s.sftp_put('a', 'b')
    with pytest.raises(SSHException):
        s.sftp_get('a', 'b')


def test_context_manager_invokes_connect_and_close(monkeypatch):
    monkeypatch.setattr(paramiko, 'Agent', lambda: type('A', (), {'get_keys': lambda self: ['k']})())
    s = SSH('h', 'u', password='p', connect=False)
    called = {'connect': False, 'close': False}
    setattr(s, '_SSH__alive', lambda: False)

    def fake_connect(timeout=0.5):
        called['connect'] = True

    def fake_close():
        called['close'] = True

    setattr(s, '_SSH__connect', fake_connect)
    setattr(s, '_SSH__close', fake_close)
    with s:
        assert called['connect'] is True
    assert called['close'] is True
