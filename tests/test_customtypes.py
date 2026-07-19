from sshreader.customtypes import Command, EnvVars


def test_command_namedtuple_fields():
    c = Command(cmd="ls", stdout="out", stderr="err", return_code=0)
    assert c.cmd == "ls"
    assert c.stdout == "out"
    assert c.stderr == "err"
    assert c.return_code == 0


def test_envvars_namedtuple_defaults():
    e = EnvVars(username=None, agent_keys=None, dsa_key=None, ecdsa_key=None, rsa_key=None)
    assert e.username is None
    assert e.agent_keys is None