""" Typing module for sshreader
"""
# Copyright (C) 2015-2026 Jesse Almanrode
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Lesser General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Lesser General Public License for more details.
#
#     You should have received a copy of the GNU Lesser General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
from typing import NamedTuple, Optional, Union


class Command(NamedTuple):
    cmd: str
    stdout: str | bytes | None
    stderr: str | bytes | None
    return_code: int


class EnvVars(NamedTuple):
    username: str | None
    agent_keys: list | None
    dsa_key: str | None
    ecdsa_key: str | None
    rsa_key: str | None


Timeout = int | float
TimeoutTuple = tuple[Timeout, Timeout]
