#!/usr/bin/env python
# coding=utf-8
""" Copy a file to hosts enmasse
"""

from __future__ import print_function
from hostlist import expand_hostlist
import click
import sshreader
import sys

__author__ = 'Jesse Almanrode'
__version__ = '1.0'


def sftp_file(srcfile, dstfile, sjob):
    """ A pre-hook that will copy the file via sftp to the server
    contained within the pased ServerJob object

    :param srcfile: Path to local file
    :param dstfile: Path to remote file
    :param sjob: ServerJob object.
    """
    try:
        sjob._conn.sftp_put(srcfile, dstfile)
    except Exception as err:
        return err


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
@click.argument('local', nargs=1, required=True, type=click.Path(exists=True, dir_okay=False))
@click.argument('remote', nargs=1, required=True, type=click.Path(dir_okay=False))
def cli(**kwargs):
    """ Copy file to remote hosts via sftp using sshreader

    \b
    remote should be formatted like:  <hostlist_expr>:/path/to/file
    """
    if kwargs['remote'].count(':') != 1:
        raise click.BadArgumentUsage('Please enter remote like: <hostlist_expr>:/path/to/file')
    hosts, dstfile = kwargs['remote'].split(':')

    click.echo("Please enter the username and password you would like to use when logging into remote hosts")
    user = click.prompt('Username')
    passwd = click.prompt('Password', hide_input=True)

    sftp_hook = sshreader.Hook(sftp_file, args=[kwargs['local'], dstfile], ssh_established=True)
    jobs = list()
    for host in expand_hostlist(hosts):
        # I use an ls command here to "verify" the file exists after the sftp command completes.
        jobs.append(sshreader.ServerJob(host, ['ls ' + dstfile], username=user, password=passwd,
                                        prehook=sftp_hook))
    fin_jobs = sshreader.sshread(jobs, tcount=0, pcount=0)

    for job in fin_jobs:
        click.echo(job.name + ': ' + job.results[0].stdout)
    sys.exit(0)


if __name__ == '__main__':
    cli()