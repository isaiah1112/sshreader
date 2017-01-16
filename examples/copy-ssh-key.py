#!/usr/bin/env python
# coding=utf-8
""" Copy your public ssh key to a remote host
"""

from __future__ import print_function
from hostlist import expand_hostlist
import click
import sshreader
import sys

__author__ = 'Jesse Almanrode'
__version__ = '1.0'


def validate_hostlist(ctx, param, value):
    """ Callback for click to expand hostlist expressions or error

    :param ctx: Click context
    :param param: Parameter Name
    :param value: Hostlist expression to expand
    :return: List of expanded hosts
    """
    try:
        return expand_hostlist(value)
    except Exception:
        raise click.BadOptionUsage('Invalid hostlist expression')


@click.command()
@click.version_option(version=__version__)
@click.option('--hostlist', '-w', type=str, required=True, callback=validate_hostlist, help='Hostlist expression')
def cli(**kwargs):
    """ Copy ssh public key to remote hosts
    """
    sshenv = sshreader.envvars()
    
    if sshenv.rsa_key is None and sshenv.dsa_key is None:
        raise click.ClickException('Unable to find a valid ssh key')

    click.echo("Please enter the username and password to copy the ssh key to on remote hosts")
    user = click.prompt('Username')
    passwd = click.prompt('Password', hide_input=True)

    if sshenv.rsa_key is not None:
        with open(sshenv.rsa_key + '.pub') as f:
            ssh_pubkey = f.read()
    else:
        with open(sshenv.dsa_key + '.pub') as f:
            ssh_pubkey = f.read()
    with click.progressbar(kwargs['hostlist'], label='Copying ssh keys to remote hosts') as bar:
        for host in bar:
            with sshreader.SSH(host, username=user, password=passwd) as s:
                s.ssh_command('mkdir ~/.ssh && chmod 700 ~/.ssh')
                s.ssh_command('echo "' + ssh_pubkey + '" >> ~/.ssh/authorized_keys')
    sys.exit(0)

if __name__ == '__main__':
    cli()