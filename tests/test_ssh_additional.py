import paramiko

from sshreader.ssh import SSH


def test_ssh_command_timeout_branches(monkeypatch):
    # Ensure Agent has keys
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

    # combine=False -> stderr gets 'command timed out'
    res = s.ssh_command('cmd', combine=False)
    assert res.return_code == 124
    assert 'command timed out' in (res.stderr or '')

    # combine=True -> stdout gets 'command timed out'
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

    try:
        s.sftp_put('a', 'b')
        raised = False
    except SSHException:
        raised = True
    assert raised

    try:
        s.sftp_get('a', 'b')
        raised2 = False
    except SSHException:
        raised2 = True
    assert raised2


def test_context_manager_invokes_connect_and_close(monkeypatch):
    monkeypatch.setattr(paramiko, 'Agent', lambda: type('A', (), {'get_keys': lambda self: ['k']})())
    s = SSH('h', 'u', password='p', connect=False)

    called = {'connect': False, 'close': False}

    # Replace private methods on the instance
    setattr(s, '_SSH__alive', lambda: False)

    def fake_connect(timeout=0.5):
        called['connect'] = True

    def fake_close():
        called['close'] = True

    setattr(s, '_SSH__connect', fake_connect)
    setattr(s, '_SSH__close', fake_close)

    with s:
        # inside context, connect should have been called
        assert called['connect'] is True

    # on exit, close should have been called
    assert called['close'] is True
