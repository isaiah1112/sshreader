# Changelog

## Release release/v4.0
 * Refactor work for package. [f612acc]
 * Setting up objects to have proper __str__ function [89682ca]
 * Rewriting logic in ServerJob class functions. [d18e37a]
 * Fixing errors in integration tests. [4324883]
 * Cleaning up code in sshreader.Hook class. [65adfa9]
 * Adding ability to pass private keyfile password to paramiko. [af3390a]
 * If you haven't moved from Python 3.5 to 3.6 then you are living in the dark ages. [c010419]
 * Added ability to run pre/post hooks while SSH connection is established. [f711a23]
 * Updating Hook documentation. [8eb3140]
 * Fixing location of posthook when runlocal is set to true [006d8ea]
 * Setting up bitbucket pipelines. [592d090]
 * Updated requirements and version [6d0bd75]

## Version 3.7.4
 * Fixing bug when cpu_count() for a machine is 1 that causes cpusoftlimit() to return 0. [67133a4]

## Version 3.7.3
 * Updated documentation hosting [ec1f6f9]

## Version 3.7.2
 * Fixing bug in pydsh if script file is empty [b075256]

## Version 3.7.1
 * Fixing bug in sshreader.ssh.envvars() method [d24fe51]

## Version 3.7
 * Added ability to run script file via pydsh. [9bd476e]
 * Increasing threadlimit [1e07336]
 * Updated redline help in pydsh. [7bd1f82]
 * Expanded ability for running script files remotely. [5fb6172]
 * Catching errors in SFTP pre-hook. [5112dee]
 * Fixing Hook.run so that additional args/kwargs are appended to the existing ones. [158db6f]
 * Added is_alive check for ssh connection on sftp_put and sftp_get [d39a30d]
 * Fixing bug when sftp exception occurs that sftp connection doesnt get closed. [7b716aa]
 * Changing ServerJob.print() to ServerJob.output() [e5d1f28]
 * Converting dict to named tuple for sshreader.ssh.envvars() method [46e0bba]
 * Updated Requirements and Version [4381413]

## Version 3.6
 * Automating testing with tox [0be301e]
 * Adding creation of .ssh directory for copy-ssh-key example script. [eedc862]
 * Updated Python versions SSHreader is tested against. [c6a108f]
 * Updating methodology for determining tcount dynamically.  Things should scale nicer now. [e03c3b8]
 * Can you say “code cleanup”?  This will make things better in the long run! [a95a6d8]
 * Changing ssh_public_key_path to ssh_key_path in unit tests for sshreader. [081aabe]
 * Added docs env to tox for testing documentation builds. [ae1fbc2]
 * Added support for ECDSA ssh key discovery in envvars method [b239dfd]
 * Renaming SSH.connection to SSH._connection. [7d0fad2]
 * Updating unittests to increase speed. [aacb7c7]

## Version 3.5.1
 * Updated SSH.ssh_command to capture timeouts properly and return errors gracefully. [fdfba44]
 * Increased Timeout to 10 Minutes [858f048]
 * Fixing small bug with assignment of NamedTuple [2d82fa1]
 * Updating unit/integration tests to prompt for params initially and save them for future runs. [abd8c34]
 * Fixing bugs in tests in Python2.7 [d5ff0b7]

## Version 3.5
 * Updated pydsh so that commands that do not return any output are not displayed.  Closes issue #12 [48d376c]
 * Pydsh 2.0.  Works more like pdsh but now includes ability to perform dshbak grouping and coalescing within the tool! [3277bb5]
 * Adding example script for copying ssh key to remote hosts. Created new examples directory! [86323da]
 * Updated documentation to include more Getting Started examples [b9d884d]
 * Exiting cli properly in pydsh [d8d3e08]
 * Silencing paramiko logging to better handle pre-connection errors that occur when openSSH cannot complete handshake.  Exceptions are still passed but log entries are silenced. [3d4a893]
 * Moving to Python logging module for INFO and DEBUG statements [caafc6f]
 * Updated pydsh debug to enable logging level INFO [510e16b]

## Version 3.4.6
 * Adding pseudo terminal creation to ssh_command method. It already existed for when output is combined. Closes issue #11 [6d85e77]

## Version 3.4.5
 * Changing default thread limit to 100 rather than 500 [211531d]
 * Fixing bug with ServerJob.print() method [084b377]

## Version 3.4.4
 * Updated echo method to flush stdout after every print.  This will allow for better access to unbuffered output. Closes issue #10 [604e6e7]

## Version 3.4.3
 * Fixing mixed tabs. [086d94f]
 * Refactoring debuglevels and making ssh connection errors more apparent. Closes issue #9 [7f2e79b]
 * Updating requirements! [c694370]

## Version 3.4.2
 * Not documenting private members. [0d91962]
 * Updated examples in Getting Started [7ac82bb]
 * Added validate_expr callback for click to expand hostlist expressions. [8f2e37b]

## Version 3.4
 * Updated FAQ for byte string vs unicode string to include new default behavior for sshreader. [009258e]
 * Beginning to add sftp commands to SSH class for extended abilities within sshreader. [2ede38b]
 * Updated requirements for sshreader. [fabc179]
 * Updated documentation version. [1d541dc]
 * Removing extra debug statements [9375187]
 * Removing hostname from 'Unable to establish connection' message. [10a9591]
 * Removing sshreader from requirements file. [7a43f6d]
 * Protecting class methods within SSH (so it can be subclassed if needed) [680c0df]
 * Updated README file [2c11c62]
 * You typo 1 thing and it all falls apart! smh [2b2b860]
 * Go bold or go home! [982bf7e]
 * Updated package version. [ba29bce]
 * Updated docs. [e04c9ee]
 * Updated Requirements. [6874fc5]
 * dirty hack, have a better idea ? [66b8902]

## Version 3.3
 * Added --redline option to run sshreader at hardCPULimit [b9f4530]
 * Rewrote pydsh to use Click library for argument parsing.  Some flags have changed! [80d8e2c]
 * Removing sort option and cleaning up logic. [dbdfe90]
 * Added examples to help epilog [bd4a3c0]
 * Rewrote printjobs and dshbak hooks [9ad72dc]
 * Updated keyfile and password preference logic. [f10098a]
 * Added cpusoftlimit and cpuhardlimit methods that return number of sub-processes your system is allowed to spawn. [4145a89]
 * Bumping pydsh version to 1.3 [6ba7de7]
 * Testing cpusoftlimit and cpuhardlimit methods. [b701489]
 * Debug output can let you know how many sub-processes your system might use while running pydsh. [54374ce]
 * Updating print_results method to print [1028856]
 * Updated deprecation messages. [007ece6]
 * Not looping over lines in default output. [49a347c]
 * Moving print statements to click wrapper [d0e9e7a]
 * Changing timeout for SSH commands to default at 300 seconds [5a649b6]
 * Changed decode bytes option to True by default [13a2b2a]

## Version 3.2
 * Added echo method that implements a multiprocessing.Lock object for print. [7216411]
 * Implementing a thread limit when using pcount and tcount in conjuction when tcount == 0.  This limits each process to automatically launching 500 each. [ac0c413]
 * Limiting threads to 500 when tcount=0 and pcount=None. [c5ef02c]
 * Restructuring methodology for implementing thread limit when only using threads. [156c9a0]
 * Added warnings for exceeding threadlimit [808a5d4]
 * Adding documentation for getting started. [5ab175f]
 * Added envvars method which attempts to gather username and ssh_key info from OS. [6911582]

## Version 3.1
 * Using os and getpass modules in conjunction when determining username. [1199c86]
 * Added decodebytes flag to ssh_command and shell_command for decoding byte-strings to unicode-strings. This can help with compatibility when using Python 3. [86a7ed0]
 * Using all unicode_literals because, well, because I said so! [7c247e9]
 * Added unicode strings FAQ. [3d76108]
 * Added timeout flag to pydsh cli so it can be overriden for long running commands. [2999e5c]

# Version 3.0.1
 * Fixed typo in ssh docstring [328bb5c]
 * SSH class can now be used with Python 'with' statement [f54ac3d]

# Version 3.0
 * Now works with Python2.7 and Python3.5!
 * Added pydsh script (installs in /usr/local/bin) (Python implemenation of pdsh that uses sshreader) [1cbf65a]
 * Now using progressbar2 module for progress bar in sshread method! [e9431e0]
 * Initial Unittests... Many more to come! [9d1996f]
 * Created new Hook class for working with pre and post hooks. [473051a]
 * Major rework of how sub-processes and threads are generated/managed. [160fecf]
 * Moved do\_shell\_script to shell\_command to match ssh\_command from SSH class.  do\_shell\_script will be removed in sshreader v4.0 [de4523d]
 * Removed tprint function. [ea90405]
 * Removed ability to override prehook, posthook, and debuglevel via the sshread method.  Set them at the ServerJob level. [160fecf]
 * Added connect kwarg to SSH class and testing for established connection when issuing ssh\_command. [35f5d24]
 * Silencing progress\_bar when used in conjunction with debuglevel. [dab6ac2]
 * Fixed issue with not closing file specification from Popen. [af1c641]
 * Fixed bug if keyfile is not set when initializing SSH object. [46ac270]
 * Added return\_code to ShellCommand namedtuple. [182570b]
 * ServerJob.status now is a sum of return codes from each cmd in the job (a status of 255 means ssh did not connect). [182570b]
 * Removed ServerJob.cmdStatus and renamed ServerJob.cmdResults to ServerJob.results [182570b]
 * Renamed ServerJob.ssh\_con to ServerJob.\_conn [c4fe4b5]
 * Added FAQ to docs for including helpful hints. [f7139c6]

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
 * Fixed bug where Paramiko was searching user SSH keys (we require a manually specified key location)
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
