import click

import sshreader
from sshreader.scripts import pydsh
from sshreader.customtypes import Command


def test_copy_script_success():
    class Conn:
        def sftp_put(self, src, dst):
            return True

    class Job:
        def __init__(self):
            self._conn = Conn()
            self.name = 'host'

    job = Job()
    assert pydsh.copy_script('/tmp/fake', job) is True


def test_copy_script_failure(monkeypatch):
    class Conn:
        def sftp_put(self, src, dst):
            raise RuntimeError('fail')

    job = type('J', (), {'_conn': Conn(), 'name': 'h'})()
    assert pydsh.copy_script('/tmp/fake', job) is False


def test_output_and_dshbak_and_coalesce(monkeypatch, capsys):
    # Prepare jobs
    job1 = type('J', (), {})()
    job1.name = 'h1'
    job1.status = 0
    job1.results = [Command('cmd', 'a\nb', None, 0)]

    job2 = type('J', (), {})()
    job2.name = 'h2'
    job2.status = 0
    job2.results = [Command('cmd', 'a\nb', None, 0)]

    # Capture echo outputs via sshreader.echo
    collected = []

    def fake_echo(s):
        collected.append(s)

    monkeypatch.setattr(sshreader, 'echo', fake_echo)
    pydsh.output(job1)
    assert any('h1:' in c for c in collected)

    # Test dshbak (uses click.echo -> capsys)
    pydsh.dshbak([job1])
    out = capsys.readouterr().out
    assert 'h1' in out
    assert 'a' in out

    # Test coalesce groups identical output
    pydsh.coalesce([job1, job2])
    out2 = capsys.readouterr().out
    assert 'a' in out2


def test_validate_hostlist_good_and_bad():
    # good
    res = pydsh.validate_hostlist(None, 'hosts', 'host[1-2]')
    assert isinstance(res, list)
    # bad
    try:
        pydsh.validate_hostlist(None, 'hosts', 'not_a_host[')
        raised = False
    except click.BadOptionUsage:
        raised = True
    assert raised