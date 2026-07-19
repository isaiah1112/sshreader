import os
from click.testing import CliRunner

import sshreader
from sshreader.scripts import pydsh
from sshreader.customtypes import EnvVars


def test_cli_script_file_not_found():
    runner = CliRunner()
    result = runner.invoke(pydsh.cli, ['--file', '-w', 'host1', 'nonexistent.sh'])
    assert result.exit_code != 0
    assert 'Script file not found' in result.output


def test_cli_script_without_shebang(tmp_path, monkeypatch):
    # create script without shebang
    script = tmp_path / 'script.sh'
    script.write_text('echo hello')
    # create dummy keyfile
    key = tmp_path / 'id_rsa'
    key.write_text('key')
    runner = CliRunner()
    # monkeypatch envvars to return a username so we pass that check
    monkeypatch.setattr(sshreader, 'envvars', lambda: EnvVars(username='u', agent_keys=None, dsa_key=None, ecdsa_key=None, rsa_key=None))
    result = runner.invoke(pydsh.cli, ['--file', '-w', 'host1', '-u', 'u', '-k', str(key), str(script)])
    assert result.exit_code != 0
    assert 'Script must start with #!' in result.output


def test_cli_port_invalid(monkeypatch):
    runner = CliRunner()
    # valid hostlist and username via envvars
    monkeypatch.setattr(sshreader, 'envvars', lambda: EnvVars(username='u', agent_keys=None, dsa_key=None, ecdsa_key=None, rsa_key=None))
    result = runner.invoke(pydsh.cli, ['-w', 'host1', 'uname', '--port', '-1', '-u', 'u'])
    assert result.exit_code != 0
    assert 'Please enter a positive integer' in result.output


def test_cli_missing_username_and_no_env(monkeypatch):
    runner = CliRunner()
    # envvars returns username None
    monkeypatch.setattr(sshreader, 'envvars', lambda: EnvVars(username=None, agent_keys=None, dsa_key=None, ecdsa_key=None, rsa_key=None))
    result = runner.invoke(pydsh.cli, ['-w', 'host1', 'uname'])
    assert result.exit_code != 0
    assert 'Unable to determine ssh username' in result.output


def test_cli_runs_sshread_monkeypatched(monkeypatch, tmp_path):
    # Ensure we don't spawn processes: monkeypatch sshreader.sshread
    monkeypatch.setattr(sshreader, 'envvars', lambda: EnvVars(username='u', agent_keys=None, dsa_key=None, ecdsa_key=None, rsa_key=None))
    called = {}

    def fake_sshread(jobs, *args, **kwargs):
        called['count'] = len(jobs)
        return jobs

    monkeypatch.setattr(sshreader, 'sshread', fake_sshread)
    runner = CliRunner()
    result = runner.invoke(pydsh.cli, ['-w', 'host1', '-u', 'u', '-P', 'pw', 'uname'])
    # CLI exits with sys.exit(0), which click converts to exit_code 0
    assert result.exit_code == 0
    assert called.get('count') == 1
