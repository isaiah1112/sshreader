# Changelog

# Version 3.0
 * Now works with Python2.7 and Python3.5!
 * Added pydsh script (installs in /usr/local/bin) (Python implemenation of pdsh that uses sshreader) [1cbf65a](https://bitbucket.org/isaiah1112/sshreader/commits/1cbf65a)
 * Now using progressbar2 module for progress bar in sshread method! [e9431e0](https://bitbucket.org/isaiah1112/sshreader/commits/e9431e0)
 * Initial Unittests... Many more to come! [9d1996f](https://bitbucket.org/isaiah1112/sshreader/commits/9d1996f)
 * Created new Hook class for working with pre and post hooks. [473051a](https://bitbucket.org/isaiah1112/sshreader/commits/473051a)
 * Major rework of how sub-processes and threads are generated/managed. [160fecf](https://bitbucket.org/isaiah1112/sshreader/commits/160fecf)
 * Moved do\_shell\_script to shell\_command to match ssh\_command from SSH class.  do\_shell\_script will be removed in sshreader v4.0 [de4523d](https://bitbucket.org/isaiah1112/sshreader/commits/de4523d)
 * Removed tprint function. [ea90405](https://bitbucket.org/isaiah1112/sshreader/commits/ea90405)
 * Removed ability to override prehook, posthook, and debuglevel via the sshread method.  Set them at the ServerJob level. [160fecf](https://bitbucket.org/isaiah1112/sshreader/commits/160fecf)
 * Added connect kwarg to SSH class and testing for established connection when issuing ssh\_command. [35f5d24](https://bitbucket.org/isaiah1112/sshreader/commits/35f5d24)
 * Silencing progress\_bar when used in conjunction with debuglevel. [dab6ac2](https://bitbucket.org/isaiah1112/sshreader/commits/dab6ac2)
 * Fixed issue with not closing file specification from Popen. [af1c641](https://bitbucket.org/isaiah1112/sshreader/commits/af1c641)
 * Fixed bug if keyfile is not set when initializing SSH object. [46ac270](https://bitbucket.org/isaiah1112/sshreader/commits/46ac270)
 * Added return\_code to ShellCommand namedtuple. [182570b](https://bitbucket.org/isaiah1112/sshreader/commits/182570b)
 * ServerJob.status now is a sum of return codes from each cmd in the job (a status of 255 means ssh did not connect). [182570b](https://bitbucket.org/isaiah1112/sshreader/commits/182570b)
 * Removed ServerJob.cmdStatus and renamed ServerJob.cmdResults to ServerJob.results [182570b](https://bitbucket.org/isaiah1112/sshreader/commits/182570b)
 * Renamed ServerJob.ssh\_con to ServerJob.\_conn [c4fe4b5](https://bitbucket.org/isaiah1112/sshreader/commits/c4fe4b5)
 * Added FAQ to docs for including helpful hints. [f7139c6](https://bitbucket.org/isaiah1112/sshreader/commits/f7139c6f798002d4b743e1a52d5644a446587da6)

# Version 2.3
 * Importing \_\_future\_\_ statements for print\_function and division
 * Moved into Python Package
 * Split SSH and do\_shell\_script into new ssh module
 * Rebuilt Sphinx Documentation (and cleanded up docstrings)
 * Fixed bug with ssh_command function when combining stderr and stdout
 * Fixed bug when path to keyfile was relative to `~`

# Version 2.2.1
 * Publishing as Open Source (Thank you to [Level 3 Communications](http://www.level3.com) for giving me the approval to do this!)

# Version 2.2
 * Updated pre and post hooks to dictionaries as data structure
 * Added tprint function for attempt at thread-safe printing

# Version 2.1.4
 * Fixed bug with Paramiko log file warnings

# Version 2.1.2
 * Using xrange in Python2 to speed calculation
 * Attempting to fix bug when SSH session exits dirty, causing thread to hang
 * Updating tcp transport window size for Paramiko (per https://github.com/Paramiko/Paramiko/issues/175)

# Version 2.1
 * Imposing limits on number of serverjobs and sub-processes so you don't make a system unusable
 * Added ability to set pcount to -1 for maximum performance mode
 * Fixed bug when sshread method is called multiple times with progressbar enabled

# Version 2.0
 * SSHreader supports both multi-threading and multi-processing or a combination of both

# Version 1.6
 * Fixed bugs with pre and post hook statuses
 * Fixed bug if serverjob command is not in list form
 * Fixed bug when using SSH key with custom username
 * Progress_bar now only updates when percentage changes
 * Increased verbosity with debuglevel > 2
 * Changed to multiprocessing instead of threads

# Version 1.5
 * Improved individual SSH command statuses
 * Added ability for sshread method to accept single job (in non-list form)
 * Added ability to combine stdout and stderr from commands
 * Added Queues to manage serverjob object for threads (FINALLY)

# Version 1.4.3
 * Fixed bug where progress_bar was printed with every loop
 * Fixed bug where Paramiko was searching for SSH host keys
 * Fixed bug where Paramiko was search user SSH keys (we require a manually specified key location)
 * Added shorter-style progress bar

# Version 1.4
 * Added progressbar support during job processing
 * Added pre and post hooks for threads
 * SSH results now returned as tuple
 * Added ability to reconnect to a closed SSH connection
 * Added is_alive method for SSH connections

# Version 1.3
 * Added support for spawning non-threaded SSH sessions
 * Added support for running local shell commands (do\_shell\_script function)

# Version 1.2
 * Added support for limiting number of threads to spawn

# Version 1.1
 * Fixed bug when specifying username/password for SSH
 * Added debug levels for sshreader
 * Added more exception handling
 * Fixed bug with thread status

# Version 1.0
 * Initial Version of sshreader
 * Very simple threading and control of threads
