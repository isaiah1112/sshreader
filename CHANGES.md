# Changelog

# Release 6.1
 * Ensuring Sphinx requirements are exported to `requirements.txt` [0967880]
 * Added `python3.13` to supported versions and made default [9810ece]
 * Updated requirements [6ddd72e]

## Release 6.0
 * Removed support for Python3.7
 * Added support for Python3.12
 * Added ability to include port in hostlist expression for pydsh [c5b33d9]
 * Ensuring SSH Port passed to pydsh is a positive integer [e485991]
 * Adding Timeout type to ServerJob Object [e4f368c]
 * Renamed types module to customtypes to not override internal types module [8e5a1e6]
 * Added poetry config and lock file for requirements [7ed936b]
 * Added option to disable SHA2 hashes in SSH Connections when using `pydsh` [ea06850]

## Release 5.0.4
 * Added ability to disable SHA2 RSA hashes on ServerJob objects [dc46c2a]

## Release 5.0.3
 * Fixed bug in pydsh where non-dshbak/coalesce output wasn't printed to terminal [16bdc25]

## Release 5.0.2
 * Fixed typo in pydsh which was breaking the entire tool. [cfd0fc7]

## Release 5.0.1
 * Fixing bug where pydsh script was being created properly [1f7e04c]

## Release 5.0.0
 * Dropped Python3.6 from supported versions
 * Added Python3.11 to supported versions
 * Removing failfast from SSH.connection function [0e14155]
 * Updated default timeouts in ServerJob class to 0.5s and 30s [c491d71]
 * Removed timeout flag in pydsh [05e5540]
 * Removing sleep loop waiting for task_queue to fill [2773c8c]
 * Fixed bug with leaking semaphores when using echo function with Lock object [8c93c78]
 * Configuring pydsh to use print_lock feature [ba5b419]
 * Changed up logic for joining and closing pids and threads [cd3d2e6]
 * Updated paramiko requirement to remove blowfish depreciation warnings [cf0d3d7]
 * Added typing hints to methods, classes, etc [a9d1ebf]
 * Removed tox testing (Bitbucket Pipelines does things much faster) [ac34edd]
 * Removed a number of assert statements across the utilities module [05194f4]
 * Added ability to guess at a username based on $HOME path [29408ff]
 * Configured pydsh to be an entry_point and part of the sshreader package [b0d3804]
 * Removed cpuhardlimit and threadlimit methods in favor of cpu_limit method. [566300d]
 * Adding Flake8 liniting to Makefile and Bitbucket Pipelines [9019abb]

## Release 4.9.2
 * Fixed bug with leaking semaphores for echo method [bc9422b]
 * Updated paramiko requirement to remove blowfish depreciation warnings [cf0d3d7]

## Release v4.9.1
 * Revert "Updated requirements" [25d2481]
 * This will be the last version to support Python3.6

## Release v4.9.0
 * Updated log levels for ssh key messages in pydsh [ec9639e]
 * Added support for enabling RSA SHA2 algorithms via Paramiko's methodology [50ceaac]
 
## Release v4.8.2
 * Updating classifier [4529041]
 * Updated check for Python3.6 or later [4a4702c]
 * Updated copyright [5dded5b]
 * Updated requirements [123b2eb]

## Release v4.8.1
 * Removing support for Python3.5 [c9f5f89]

## Release v4.8.0
 * Using twine to upload to PyPI. [290baa2]
 * Adding Python3.10 to testing [47128ab]
 * Updated requirements and documentation version [2f18080]

## Release v4.7.0
 * Removing Python2 code [481422f]
 * Added Python3.9 to testing [ca50dc7]
 * Added Makefile with commands for building/pushing docker image. [7be1fb3]
 * Not returning value for sftp.get since it returns nothing. [fd576b1]

## Release v4.6.0
 * Updated paramiko to 2.6.0 to remove cryptography warnings [93311e7]
 * Added python 3.8 to testing suite [02d507f]
 * Code cleanup in pydsh [c68aba3]
 * Updated error string [97abf50]
 * Fixed bug when task_queue is not full when sub-process or thread is spawned. [4533f4d]
 * Fixed multiprocessing issue when using 'fork' to spawn child processes [96d69a6]
 * Disabled item_counter semaphore if not using progress bar [26b6e20]
 * Removed support for Python2.7 [1fc8b09]
 * Testing yaml anchors in bitbucket-pipelines.yml [1165b33]
 * Updated version compatibility checking across module. [6aaa365]

## Release v4.5.3
 * Updated python-hostlist requirement in setup.py [dcb6004]

## Release v4.5.2
 * Removed Python3.4 Support [e427ee2]

## Release v4.5.1
 * Updated paramiko to 2.6.0 to remove cryptography warnings [c0828ae]

## Release v4.5.0
 * Fixing tox command for py37 [ffbf342]
 * Created custom configuration for sshreader logging. [31486dd]
 * Added verbosity setting for debug logging in pydsh [f39254e]
 * Updated requirements [b5f8ed6]

## Release v4.4.4
 * Fixing bug when ssh dies while command is running [81b2a88]

## Release v4.4.3
 * Wrapping ssh_command in try statement during multiprocessing/threading [4127792]

## Release v4.4.2
 * Ensuring that ssh.\_conn is always None when job exits [c6ebcb4]

## Release v4.4.1
 * Adding Python3.7 to test suite [b64acd9]
 * Updated requirements [7558423]
 * Adding Python3.7 to supported python versions [2346828]

## Release v4.4.0
 * Updating setup.py information [352834d]
 * Bringing Python3.4 and Python 3.5 back into testing. [c5ffcc8]
 * Automated testing with tox using Bitbucket Pipelines [91bfc28]
 * Allowing local testing as well as testing with Bitbucket Pipelines [39803cf]
 * Added step for building documentation on master branch pipelines [c966372]
 * Added failfast param to docstring [212815b]
 * Testing keyfile as str. Refactored ssh connection timeout. Updated cmd timeout error [9854f39]
 * Updating integration tests to include new return codes. [e3879f6]
 * Updated timeout code to 124 [7793407]

## Release v4.3.3
 * Limiting number of ServerJob objects in integration tests [a3f18d3]
 * Attempting to fix bug in Python 3.4 where join never completes for sub-processes [538a4d8]
 * Fixing bug with Hook class when asking for __str__ method. [f78f51f]
 * Cleaning up logging statements [2878e4d]

## Release v4.3.2
 * Revert "Updated logic to actually update kwargs for sshreader.Hook class" [491ee60]

## Release v4.3.1
 * Ensuring pydsh prefers threads by default [70b9974]

## Release v4.3.0
 * Updated pydsh to prefer threading by default [d512b97]
 * Updated logic to actually update kwargs for sshreader.Hook class [1791486]
 * Refactoring logging in sshreader.ServerJob class [a4fba76]
 * Updated logic for waiting for threads/processes to close in sshreader.sshread method [edb257f]
 * Allowing control over threadlimitfactor in sshreader. [eb6108c]

## Release v4.2.1
 * Added failfast flag to SSH.connect [75ac26e]
 * More code cleanup [a98bdc3]

## Release v4.2.0
 * Added socket open check to SSH.connect [8af9c6e]
 * Added example of parallel-sftp.py [fc4acef]
 * Code cleanup [6793a20]
 * Bugs found and fixed.  Tests updated. [625b2ee]
 * Updated requirements and version number [a3e622b]

## Release v4.1.2
 * Fixing bug in pydsh when detecting SSH Agent keys [614d5e9]

## Release v4.1.1
 * Fixing bug where ServerJob doesn't detect SSH Agent Keys. [7298771]

## Release v4.1.0
 * Updating SSH.sftp\_get and SSH.sftp\_put methods to ensure sftp transport is closed regardless of whether an exception occurs. [d7a1ced]
 * Moved enabling of debug logging higher in pydsh initialization. [60dc90c]
 * Update logger variable. [219435c]
 * Configuring SSH class to use SSH Agent for ssh private key discovery. [bd7ffa0]
 * Updated pydsh to work with SSH Agent key detection. [e9a1f1f]
 * Added some logging to pydsh. [d6b9950]
 * Updated Requirements [693e0f5]

## Release v4.0.1
 * Fixing bitbucket-pipelines script. [163c513]
 * Fixing documentation formatting [6ae0153]
 * Fixing typo in CHANGES.md [0ea4ee1]
 * Added ability to specify SSH port when using pydsh. [8df2365]
 * Updated Requirements [b8555b1]

## Release v4.0.0
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

## Release v3.7.4
 * Fixing bug when cpu\_count() for a machine is 1 that causes cpusoftlimit() to return 0. [67133a4]

## Release v3.7.3
 * Updated documentation hosting [ec1f6f9]

## Release v3.7.2
 * Fixing bug in pydsh if script file is empty [b075256]

## Release v3.7.1
 * Fixing bug in sshreader.ssh.envvars() method [d24fe51]

## Release v3.7.0
 * Added ability to run script file via pydsh. [9bd476e]
 * Increasing threadlimit [1e07336]
 * Updated redline help in pydsh. [7bd1f82]
 * Expanded ability for running script files remotely. [5fb6172]
 * Catching errors in SFTP pre-hook. [5112dee]
 * Fixing Hook.run so that additional args/kwargs are appended to the existing ones. [158db6f]
 * Added is\_alive check for ssh connection on sftp\_put and sftp\_get [d39a30d]
 * Fixing bug when sftp exception occurs that sftp connection doesnt get closed. [7b716aa]
 * Changing ServerJob.print() to ServerJob.output() [e5d1f28]
 * Converting dict to named tuple for sshreader.ssh.envvars() method [46e0bba]
 * Updated Requirements and Version [4381413]

## Release v3.6.0
 * Automating testing with tox [0be301e]
 * Adding creation of .ssh directory for copy-ssh-key example script. [eedc862]
 * Updated Python versions SSHreader is tested against. [c6a108f]
 * Updating methodology for determining tcount dynamically.  Things should scale nicer now. [e03c3b8]
 * Can you say “code cleanup”?  This will make things better in the long run! [a95a6d8]
 * Changing ssh\_public\_key\_path to ssh\_key\_path in unit tests for sshreader. [081aabe]
 * Added docs env to tox for testing documentation builds. [ae1fbc2]
 * Added support for ECDSA ssh key discovery in envvars method [b239dfd]
 * Renaming SSH.connection to SSH.\_connection. [7d0fad2]
 * Updating unittests to increase speed. [aacb7c7]

## Release v3.5.1
 * Updated SSH.ssh_command to capture timeouts properly and return errors gracefully. [fdfba44]
 * Increased Timeout to 10 Minutes [858f048]
 * Fixing small bug with assignment of NamedTuple [2d82fa1]
 * Updating unit/integration tests to prompt for params initially and save them for future runs. [abd8c34]
 * Fixing bugs in tests in Python2.7 [d5ff0b7]

## Release v3.5.0
 * Updated pydsh so that commands that do not return any output are not displayed.  Closes issue #12 [48d376c]
 * Pydsh 2.0.  Works more like pdsh but now includes ability to perform dshbak grouping and coalescing within the tool! [3277bb5]
 * Adding example script for copying ssh key to remote hosts. Created new examples directory! [86323da]
 * Updated documentation to include more Getting Started examples [b9d884d]
 * Exiting cli properly in pydsh [d8d3e08]
 * Silencing paramiko logging to better handle pre-connection errors that occur when openSSH cannot complete handshake.  Exceptions are still passed but log entries are silenced. [3d4a893]
 * Moving to Python logging module for INFO and DEBUG statements [caafc6f]
 * Updated pydsh debug to enable logging level INFO [510e16b]

## Release v3.4.6
 * Adding pseudo terminal creation to ssh\_command method. It already existed for when output is combined. Closes issue #11 [6d85e77]

## Release v3.4.5
 * Changing default thread limit to 100 rather than 500 [211531d]
 * Fixing bug with ServerJob.print() method [084b377]

## Release v3.4.4
 * Updated echo method to flush stdout after every print.  This will allow for better access to unbuffered output. Closes issue #10 [604e6e7]

## Release v3.4.3
 * Fixing mixed tabs. [086d94f]
 * Refactoring debuglevels and making ssh connection errors more apparent. Closes issue #9 [7f2e79b]
 * Updating requirements! [c694370]

## Release v3.4.2
 * Not documenting private members. [0d91962]
 * Updated examples in Getting Started [7ac82bb]
 * Added validate_expr callback for click to expand hostlist expressions. [8f2e37b]

## Release v3.4.0
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

## Release v3.3.0
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
 * Updating print\_results method to print [1028856]
 * Updated deprecation messages. [007ece6]
 * Not looping over lines in default output. [49a347c]
 * Moving print statements to click wrapper [d0e9e7a]
 * Changing timeout for SSH commands to default at 300 seconds [5a649b6]
 * Changed decode bytes option to True by default [13a2b2a]

## Release v3.2.0
 * Added echo method that implements a multiprocessing.Lock object for print. [7216411]
 * Implementing a thread limit when using pcount and tcount in conjuction when tcount == 0.  This limits each process to automatically launching 500 each. [ac0c413]
 * Limiting threads to 500 when tcount=0 and pcount=None. [c5ef02c]
 * Restructuring methodology for implementing thread limit when only using threads. [156c9a0]
 * Added warnings for exceeding threadlimit [808a5d4]
 * Adding documentation for getting started. [5ab175f]
 * Added envvars method which attempts to gather username and ssh\_key info from OS. [6911582]

## Release v3.1.0
 * Using os and getpass modules in conjunction when determining username. [1199c86]
 * Added decodebytes flag to ssh\_command and shell\_command for decoding byte-strings to unicode-strings. This can help with compatibility when using Python 3. [86a7ed0]
 * Using all unicode\_literals because, well, because I said so! [7c247e9]
 * Added unicode strings FAQ. [3d76108]
 * Added timeout flag to pydsh cli so it can be overriden for long running commands. [2999e5c]

# Version 3.0.1
 * Fixed typo in ssh docstring [328bb5c]
 * SSH class can now be used with Python 'with' statement [f54ac3d]

# Version 3.0.0
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

# Version 2.3.0
 * Importing \_\_future\_\_ statements for print\_function and division
 * Moved into Python Package
 * Split SSH and do\_shell\_script into new ssh module
 * Rebuilt Sphinx Documentation (and cleanded up docstrings)
 * Fixed bug with ssh_command function when combining stderr and stdout
 * Fixed bug when path to keyfile was relative to `~`

# Version 2.2.1
 * Publishing as Open Source (Thank you to [Level 3 Communications](http://www.level3.com) for giving me the approval to do this!)

# Version 2.2.0
 * Updated pre and post hooks to dictionaries as data structure
 * Added tprint function for attempt at thread-safe printing

# Version 2.1.4
 * Fixed bug with Paramiko log file warnings

# Version 2.1.2
 * Using xrange in Python2 to speed calculation
 * Attempting to fix bug when SSH session exits dirty, causing thread to hang
 * Updating tcp transport window size for Paramiko (per https://github.com/Paramiko/Paramiko/issues/175)

# Version 2.1.0
 * Imposing limits on number of serverjobs and sub-processes so you don't make a system unusable
 * Added ability to set pcount to -1 for maximum performance mode
 * Fixed bug when sshread method is called multiple times with progressbar enabled

# Version 2.0.0
 * SSHreader supports both multi-threading and multi-processing or a combination of both

# Version 1.6.0
 * Fixed bugs with pre and post hook statuses
 * Fixed bug if serverjob command is not in list form
 * Fixed bug when using SSH key with custom username
 * Progress_bar now only updates when percentage changes
 * Increased verbosity with debuglevel > 2
 * Changed to multiprocessing instead of threads

# Version 1.5.0
 * Improved individual SSH command statuses
 * Added ability for sshread method to accept single job (in non-list form)
 * Added ability to combine stdout and stderr from commands
 * Added Queues to manage serverjob object for threads (FINALLY)

# Version 1.4.3
 * Fixed bug where progress_bar was printed with every loop
 * Fixed bug where Paramiko was searching for SSH host keys
 * Fixed bug where Paramiko was searching user SSH keys (we require a manually specified key location)
 * Added shorter-style progress bar

# Version 1.4.0
 * Added progressbar support during job processing
 * Added pre and post hooks for threads
 * SSH results now returned as tuple
 * Added ability to reconnect to a closed SSH connection
 * Added is_alive method for SSH connections

# Version 1.3.0
 * Added support for spawning non-threaded SSH sessions
 * Added support for running local shell commands (do\_shell\_script function)

# Version 1.2.0
 * Added support for limiting number of threads to spawn

# Version 1.1.0
 * Fixed bug when specifying username/password for SSH
 * Added debug levels for sshreader
 * Added more exception handling
 * Fixed bug with thread status

# Version 1.0.0
 * Initial Version of sshreader
 * Very simple threading and control of threads
