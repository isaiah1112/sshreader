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
    assert 'is not in the range 1<=x<=65535' in result.output


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


def test_cli_timeout_option_default(monkeypatch):
    """Test that default timeout is 30 seconds"""
    monkeypatch.setattr(sshreader, 'envvars', lambda: EnvVars(username='u', agent_keys=None, dsa_key=None, ecdsa_key=None, rsa_key=None))
    captured_jobs = []

    def fake_sshread(jobs, *args, **kwargs):
        captured_jobs.extend(jobs)
        return jobs

    monkeypatch.setattr(sshreader, 'sshread', fake_sshread)
    runner = CliRunner()
    result = runner.invoke(pydsh.cli, ['-w', 'host1', '-u', 'u', '-P', 'pw', 'uname'])
    assert result.exit_code == 0
    assert len(captured_jobs) == 1
    # Check that timeout was passed (cmd_timeout should be 30)
    assert captured_jobs[0].cmd_timeout == 30


def test_cli_timeout_option_custom(monkeypatch):
    """Test that custom timeout value is applied"""
    monkeypatch.setattr(sshreader, 'envvars', lambda: EnvVars(username='u', agent_keys=None, dsa_key=None, ecdsa_key=None, rsa_key=None))
    captured_jobs = []

    def fake_sshread(jobs, *args, **kwargs):
        captured_jobs.extend(jobs)
        return jobs

    monkeypatch.setattr(sshreader, 'sshread', fake_sshread)
    runner = CliRunner()
    result = runner.invoke(pydsh.cli, ['-w', 'host1', '-u', 'u', '-P', 'pw', '--timeout', '60', 'uname'])
    assert result.exit_code == 0
    assert len(captured_jobs) == 1
    assert captured_jobs[0].cmd_timeout == 60


def test_cli_timeout_invalid(monkeypatch):
    """Test that invalid timeout values are rejected"""
    runner = CliRunner()
    monkeypatch.setattr(sshreader, 'envvars', lambda: EnvVars(username='u', agent_keys=None, dsa_key=None, ecdsa_key=None, rsa_key=None))
    result = runner.invoke(pydsh.cli, ['-w', 'host1', 'uname', '--timeout', '0', '-u', 'u'])
    assert result.exit_code != 0
    assert 'is not in the range 1<=x<=3600' in result.output


def test_cli_script_with_confirm_flag(tmp_path, monkeypatch):
    """Test script execution with --confirm flag (no prompt)"""
    script = tmp_path / 'script.sh'
    script.write_text('#!/bin/bash\necho hello')
    key = tmp_path / 'id_rsa'
    key.write_text('key')
    
    monkeypatch.setattr(sshreader, 'envvars', lambda: EnvVars(username='u', agent_keys=None, dsa_key=None, ecdsa_key=None, rsa_key=None))
    captured_jobs = []

    def fake_sshread(jobs, *args, **kwargs):
        captured_jobs.extend(jobs)
        return jobs

    monkeypatch.setattr(sshreader, 'sshread', fake_sshread)
    runner = CliRunner()
    result = runner.invoke(pydsh.cli, [
        '--file', '--confirm', '-w', 'host1', '-u', 'u', '-k', str(key), str(script)
    ])
    assert result.exit_code == 0
    # Should not contain confirmation prompt
    assert 'Execute this script' not in result.output


def test_cli_script_without_confirm_flag_abort(tmp_path, monkeypatch):
    """Test script execution with user declining confirmation"""
    script = tmp_path / 'script.sh'
    script.write_text('#!/bin/bash\necho hello')
    key = tmp_path / 'id_rsa'
    key.write_text('key')
    
    monkeypatch.setattr(sshreader, 'envvars', lambda: EnvVars(username='u', agent_keys=None, dsa_key=None, ecdsa_key=None, rsa_key=None))
    runner = CliRunner()
    # Simulate user choosing 'n' for confirmation
    result = runner.invoke(pydsh.cli, [
        '--file', '-w', 'host1', '-u', 'u', '-k', str(key), str(script)
    ], input='n\n')
    assert result.exit_code != 0
    assert 'Aborted' in result.output


def test_setup_script_file_not_file():
    """Test setup_script_file returns cmd unchanged when file_flag is False"""
    cmd, prehook = pydsh.setup_script_file('echo hello', False, False)
    assert cmd == 'echo hello'
    assert prehook is None


def test_setup_script_file_missing():
    """Test setup_script_file raises error for missing file"""
    try:
        pydsh.setup_script_file('/nonexistent/file.sh', True, False)
        raised = False
    except pydsh.click.BadParameter as e:
        raised = True
        assert 'Script file not found' in str(e)
    assert raised


def test_setup_script_file_no_shebang(tmp_path):
    """Test setup_script_file raises error for script without shebang"""
    script = tmp_path / 'script.sh'
    script.write_text('echo hello')
    try:
        pydsh.setup_script_file(str(script), True, False)
        raised = False
    except pydsh.click.UsageError as e:
        raised = True
        assert 'Script must start with #!' in str(e)
    assert raised


def test_create_jobs_single_host(monkeypatch):
    """Test create_jobs creates a single job"""
    def fake_job_class(*args, **kwargs):
        job = type('Job', (), {'ssh_port': 22})()
        for key, value in kwargs.items():
            setattr(job, key, value)
        return job
    
    monkeypatch.setattr(sshreader, 'ServerJob', fake_job_class)
    jobs = pydsh.create_jobs(
        hostlist=['host1'],
        cmd='uname',
        username='user',
        password='pw',
        keyfile=None,
        keypass=None,
        port=22,
        timeout=30,
        sha2=True,
        prehook=None,
        posthook=None,
        file_flag=False
    )
    assert len(jobs) == 1
    assert jobs[0].username == 'user'
    assert jobs[0].password == 'pw'


def test_create_jobs_multiple_hosts(monkeypatch):
    """Test create_jobs creates multiple jobs"""
    def fake_job_class(*args, **kwargs):
        job = type('Job', (), {'ssh_port': 22})()
        for key, value in kwargs.items():
            setattr(job, key, value)
        return job
    
    monkeypatch.setattr(sshreader, 'ServerJob', fake_job_class)
    jobs = pydsh.create_jobs(
        hostlist=['host1', 'host2', 'host3'],
        cmd='uname',
        username='user',
        password='pw',
        keyfile=None,
        keypass=None,
        port=22,
        timeout=30,
        sha2=True,
        prehook=None,
        posthook=None,
        file_flag=False
    )
    assert len(jobs) == 3


def test_create_jobs_with_port_in_hostname(monkeypatch):
    """Test create_jobs handles host:port notation"""
    job_ssh_ports = []
    
    def fake_job_class(*args, **kwargs):
        job = type('Job', (), {})()
        for key, value in kwargs.items():
            setattr(job, key, value)
        # Track ssh_port assignments
        original_setattr = job.__setattr__
        def track_setattr(name, value):
            if name == 'ssh_port':
                job_ssh_ports.append(value)
            original_setattr(name, value)
        job.__setattr__ = track_setattr
        return job
    
    monkeypatch.setattr(sshreader, 'ServerJob', fake_job_class)
    jobs = pydsh.create_jobs(
        hostlist=['host1:2222', 'host2:3333'],
        cmd='uname',
        username='user',
        password='pw',
        keyfile=None,
        keypass=None,
        port=22,
        timeout=30,
        sha2=True,
        prehook=None,
        posthook=None,
        file_flag=False
    )
    assert len(jobs) == 2


def test_execute_jobs_without_aggregation(monkeypatch):
    """Test execute_jobs with direct output (no dshbak/coalesce)"""
    sshread_called = {}
    
    def fake_sshread(jobs, *args, **kwargs):
        sshread_called['print_lock'] = kwargs.get('print_lock')
        sshread_called['progress_bar'] = kwargs.get('progress_bar')
        return jobs
    
    monkeypatch.setattr(sshreader, 'sshread', fake_sshread)
    mock_jobs = [type('Job', (), {})()]
    
    pydsh.execute_jobs(mock_jobs, False, False, False)
    assert sshread_called.get('print_lock') is True
    assert sshread_called.get('progress_bar') is None


def test_execute_jobs_with_dshbak(monkeypatch):
    """Test execute_jobs with dshbak output formatting"""
    sshread_called = {}
    
    def fake_sshread(jobs, *args, **kwargs):
        sshread_called['progress_bar'] = kwargs.get('progress_bar')
        return jobs
    
    dshbak_called = {}
    def fake_dshbak(jobs):
        dshbak_called['count'] = len(jobs)
    
    monkeypatch.setattr(sshreader, 'sshread', fake_sshread)
    monkeypatch.setattr(pydsh, 'dshbak', fake_dshbak)
    mock_jobs = [type('Job', (), {})()]
    
    pydsh.execute_jobs(mock_jobs, True, False, False)
    assert sshread_called.get('progress_bar') is True
    assert dshbak_called.get('count') == 1


def test_setup_authentication_with_no_username_provided(monkeypatch):
    """Test setup_authentication falls back to env username"""
    kwargs = {
        'username': None,
        'keyfile': None,
        'password': None,
        'prompt': False,
        'keypass': False
    }
    sshenv = EnvVars(
        username='envuser',
        agent_keys=None,
        dsa_key=None,
        ecdsa_key=None,
        rsa_key='/home/user/.ssh/id_rsa'
    )
    result = pydsh.setup_authentication(kwargs, sshenv)
    assert result['username'] == 'envuser'
    assert result['keyfile'] == '/home/user/.ssh/id_rsa'
