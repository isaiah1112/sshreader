import os
from click.testing import CliRunner

import sshreader
from sshreader.scripts import pydsh
from sshreader.customtypes import Command, EnvVars


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
    job1 = type('J', (), {})()
    job1.name = 'h1'
    job1.status = 0
    job1.results = [Command('cmd', 'a\nb', None, 0)]

    job2 = type('J', (), {})()
    job2.name = 'h2'
    job2.status = 0
    job2.results = [Command('cmd', 'a\nb', None, 0)]

    collected = []

    def fake_echo(s):
        collected.append(s)

    monkeypatch.setattr(sshreader, 'echo', fake_echo)
    pydsh.output(job1)
    assert any('h1:' in c for c in collected)

    pydsh.dshbak([job1])
    out = capsys.readouterr().out
    assert 'h1' in out
    assert 'a' in out

    pydsh.coalesce([job1, job2])
    out2 = capsys.readouterr().out
    assert 'a' in out2


def test_validate_hostlist_good_and_bad():
    res = pydsh.validate_hostlist(None, 'hosts', 'host[1-2]')
    assert isinstance(res, list)
    try:
        pydsh.validate_hostlist(None, 'hosts', 'not_a_host[')
        raised = False
    except pydsh.click.BadOptionUsage:
        raised = True
    assert raised


def test_cli_script_file_not_found():
    runner = CliRunner()
    result = runner.invoke(pydsh.cli, ['--file', '-w', 'host1', 'nonexistent.sh'])
    assert result.exit_code != 0
    assert 'Script file not found' in result.output


def test_cli_script_without_shebang(tmp_path, monkeypatch):
    script = tmp_path / 'script.sh'
    script.write_text('echo hello')
    key = tmp_path / 'id_rsa'
    key.write_text('key')
    runner = CliRunner()
    monkeypatch.setattr(sshreader, 'envvars', lambda: EnvVars(username='u', agent_keys=None, dsa_key=None, ecdsa_key=None, rsa_key=None))
    result = runner.invoke(pydsh.cli, ['--file', '-w', 'host1', '-u', 'u', '-k', str(key), str(script)])
    assert result.exit_code != 0
    assert 'Script must start with #!' in result.output


def test_cli_port_invalid(monkeypatch):
    runner = CliRunner()
    monkeypatch.setattr(sshreader, 'envvars', lambda: EnvVars(username='u', agent_keys=None, dsa_key=None, ecdsa_key=None, rsa_key=None))
    result = runner.invoke(pydsh.cli, ['-w', 'host1', 'uname', '--port', '-1', '-u', 'u'])
    assert result.exit_code != 0
    assert 'Please enter a positive integer' in result.output


def test_cli_missing_username_and_no_env(monkeypatch):
    runner = CliRunner()
    monkeypatch.setattr(sshreader, 'envvars', lambda: EnvVars(username=None, agent_keys=None, dsa_key=None, ecdsa_key=None, rsa_key=None))
    result = runner.invoke(pydsh.cli, ['-w', 'host1', 'uname'])
    assert result.exit_code != 0
    assert 'Unable to determine ssh username' in result.output


def test_cli_runs_sshread_monkeypatched(monkeypatch):
    monkeypatch.setattr(sshreader, 'envvars', lambda: EnvVars(username='u', agent_keys=None, dsa_key=None, ecdsa_key=None, rsa_key=None))
    called = {}

    def fake_sshread(jobs, *args, **kwargs):
        called['count'] = len(jobs)
        return jobs

    monkeypatch.setattr(sshreader, 'sshread', fake_sshread)
    runner = CliRunner()
    result = runner.invoke(pydsh.cli, ['-w', 'host1', '-u', 'u', '-P', 'pw', 'uname'])
    assert result.exit_code == 0
    assert called.get('count') == 1
