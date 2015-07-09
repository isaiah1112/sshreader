# [sshreader][]

## Overview

[sshreader][] is a Python module for multi-processing/threading ssh connections in order to make ssh operations
across multiple servers more parallel.  It utilizes the [paramiko][] module for its ssh client.

## License

[sshreader][] is released under the [GNU Lesser General Public License v3.0][],
see the file LICENSE and LICESE.lesser for the license text.

## Installation

Currently there is not an installation script. The most straightforward way to
get sshreader.py working is to:

  - ensure that the following modules are installed:
    - paramiko
    - logging
    - multiprocessing
    - threading
    - Queue
    - types

  - copy, move or link the file *sshreader.py*, located in the repository
    root directory, to your project directory

## Contributing

Comments and enhancements are very welcome.

Report any issues or feature requests on the [BitBucket bug
tracker](https://bitbucket.org/isaiah1112/sshreader/issues?status=new&status=open). Please include a minimal
(not-) working example which reproduces the bug and, if appropriate, the
 traceback information.  Please do not request features already being worked
towards (see the TODO file).

Code contributions are encouraged: please feel free to [fork the
project](https://bitbucket.org/isaiah1112/sshreader) and submit pull requests.


[GNU Lesser General Public License v3.0]: http://choosealicense.com/licenses/lgpl-3.0/ "LGPL v3"

[sshreader]: https://bitbucket.org/isaiah1112/sshreader "SSHreader Module"