# Changelog

## Version 3.4.4
 * Updated echo method to flush stdout after every print.  This will allow for better access to unbuffered output. Issue #10 [604e6e7](https://bitbucket.org/isaiah1112/sshreader/commits/604e6e76273c9efe53d642eadd8301e6cbe993b2)

## Version 3.4.3
 * Fixing mixed tabs. [086d94f](https://bitbucket.org/isaiah1112/sshreader/commits/086d94fb64bebc44d3aa1bbb72d8daedc571353d)
 * Refactoring debuglevels and making ssh connection errors more apparent per Issue #9 [7f2e79b](https://bitbucket.org/isaiah1112/sshreader/commits/7f2e79be15e4491164401086f903196a66610375)
 * Updating requirements! [c694370](https://bitbucket.org/isaiah1112/sshreader/commits/c694370d722b9f0b59ed06779d9d084f7e20c17c)

## Version 3.4.2
 * Not documenting private members. [0d91962](https://bitbucket.org/isaiah1112/sshreader/commits/0d9196243e4c665b191ec45b034649b0c7633c39)
 * Updated examples in Getting Started [7ac82bb](https://bitbucket.org/isaiah1112/sshreader/commits/7ac82bbc2849765d72803cd59d7247b486d3df70)
 * Added validate_expr callback for click to expand hostlist expressions. [8f2e37b](https://bitbucket.org/isaiah1112/sshreader/commits/8f2e37b89b9d9483f30b19a0d75d3c55b77bb819)

## Version 3.4
 * Updated FAQ for byte string vs unicode string to include new default behavior for sshreader. [009258e](https://bitbucket.org/isaiah1112/sshreader/commits/009258e7b375e2f8068e2e108777bc5de4851e02)
 * Beginning to add sftp commands to SSH class for extended abilities within sshreader. [2ede38b](https://bitbucket.org/isaiah1112/sshreader/commits/2ede38b2b79808dae77b421ae212047892f2d3ad)
 * Updated requirements for sshreader. [fabc179](https://bitbucket.org/isaiah1112/sshreader/commits/fabc17983e033359ce735caddc51a9b59fa5bb5a)
 * Updated documentation version. [1d541dc](https://bitbucket.org/isaiah1112/sshreader/commits/1d541dc7d0d3491a5a6d5278f720674783b716b8)
 * Removing extra debug statements [9375187](https://bitbucket.org/isaiah1112/sshreader/commits/93751876e2caf4fb718acac4bdcb269b2949d8cc)
 * Removing hostname from 'Unable to establish connection' message. [10a9591](https://bitbucket.org/isaiah1112/sshreader/commits/10a9591a234eafcf34c4fd3659ebb82d996b503e)
 * Removing sshreader from requirements file. [7a43f6d](https://bitbucket.org/isaiah1112/sshreader/commits/7a43f6dc5bb6388b7af169ddb95f2086da5ef7d8)
 * Protecting class methods within SSH (so it can be subclassed if needed) [680c0df](https://bitbucket.org/isaiah1112/sshreader/commits/680c0df606ecaabce6692526d9c7979205adedd0)
 * Updated README file [2c11c62](https://bitbucket.org/isaiah1112/sshreader/commits/2c11c62cdfc3d5b6290258160224135ab1a0e059)
 * You typo 1 thing and it all falls apart! smh [2b2b860](https://bitbucket.org/isaiah1112/sshreader/commits/2b2b860b4d9d06b42e8270a88ca864a98bb536bf)
 * Go bold or go home! [982bf7e](https://bitbucket.org/isaiah1112/sshreader/commits/982bf7e53c6ae029b0d60b8b2d6f4ddba1311395)
 * Updated package version. [ba29bce](https://bitbucket.org/isaiah1112/sshreader/commits/ba29bce4411473f1217da782259e5f7e52163375)
 * Updated docs. [e04c9ee](https://bitbucket.org/isaiah1112/sshreader/commits/e04c9eee53ed1cc26b28fccc26bdcc916763836f)
 * Updated Requirements. [6874fc5](https://bitbucket.org/isaiah1112/sshreader/commits/6874fc5cd1b35300e9b415b87197e869fa3ddd52)
 * dirty hack, have a better idea ? [66b8902](https://bitbucket.org/isaiah1112/sshreader/commits/66b89021fcaf1094f047f556954cb20150d71157)

## Version 3.3
 * Added --redline option to run sshreader at hardCPULimit [b9f4530](https://bitbucket.org/isaiah1112/sshreader/commits/b9f45307582a1169693c2824120c00c70b162bb9)
 * Rewrote pydsh to use Click library for argument parsing.  Some flags have changed! [80d8e2c](https://bitbucket.org/isaiah1112/sshreader/commits/80d8e2c55dd405320cf24a261458d8be88dfbecb)
 * Removing sort option and cleaning up logic. [dbdfe90](https://bitbucket.org/isaiah1112/sshreader/commits/dbdfe904f586553c927075ac941ac1f966a1cf79)
 * Added examples to help epilog [bd4a3c0](https://bitbucket.org/isaiah1112/sshreader/commits/bd4a3c0337f96dd3fb4eab94fa0247a6863b5057)
 * Rewrote printjobs and dshbak hooks [9ad72dc](https://bitbucket.org/isaiah1112/sshreader/commits/9ad72dcb9482f75c5c158b881c733c8bcd55a21a)
 * Updated keyfile and password preference logic. [f10098a](https://bitbucket.org/isaiah1112/sshreader/commits/f10098a0a6a3641e8885695707e0880b37c26b04)
 * Added cpusoftlimit and cpuhardlimit methods that return number of sub-processes your system is allowed to spawn. [4145a89](https://bitbucket.org/isaiah1112/sshreader/commits/4145a89d48b5570186683effbccc88af93a1df8b)
 * Bumping pydsh version to 1.3 [6ba7de7](https://bitbucket.org/isaiah1112/sshreader/commits/6ba7de74b285135fb52664925a1788e905c5dc0f)
 * Testing cpusoftlimit and cpuhardlimit methods. [b701489](https://bitbucket.org/isaiah1112/sshreader/commits/b701489b6eb24ac74529c1d0ada1bfe29f423ccb)
 * Debug output can let you know how many sub-processes your system might use while running pydsh. [54374ce](https://bitbucket.org/isaiah1112/sshreader/commits/54374cea94943d6bb8d925b0efc72c5948dac821)
 * Updating print_results method to print [1028856](https://bitbucket.org/isaiah1112/sshreader/commits/10288564451a283b9530a96d47e195134a9682f8)
 * Updated deprecation messages. [007ece6](https://bitbucket.org/isaiah1112/sshreader/commits/007ece610406a7f2caee6091987649fe949978f9)
 * Not looping over lines in default output. [49a347c](https://bitbucket.org/isaiah1112/sshreader/commits/49a347c8c165ea4d004678e346cb6ea5430fa227)
 * Moving print statements to click wrapper [d0e9e7a](https://bitbucket.org/isaiah1112/sshreader/commits/d0e9e7abde49e85f69416943c11d29a809ea933f)
 * Changing timeout for SSH commands to default at 300 seconds [5a649b6](https://bitbucket.org/isaiah1112/sshreader/commits/5a649b6292e0b29c31ed9fab37bee7941eb2e9e7)
 * Changed decode bytes option to True by default [13a2b2a](https://bitbucket.org/isaiah1112/sshreader/commits/13a2b2a08ffaba11dc41aed3c754c816df7a6306)

## Version 3.2
 * Added echo method that implements a multiprocessing.Lock object for print. [7216411](https://bitbucket.org/isaiah1112/sshreader/commits/72164116e2422b44e6704342f0bf3da855a9a054)
 * Implementing a thread limit when using pcount and tcount in conjuction when tcount == 0.  This limits each process to automatically launching 500 each. [ac0c413](https://bitbucket.org/isaiah1112/sshreader/commits/ac0c413e5c8dfc19327e846f3ad26cb766a7cb0b)
 * Limiting threads to 500 when tcount=0 and pcount=None. [c5ef02c](https://bitbucket.org/isaiah1112/sshreader/commits/c5ef02c427adcfa2e43bbd40fbabaaf4d57efa7f)
 * Restructuring methodology for implementing thread limit when only using threads. [156c9a0](https://bitbucket.org/isaiah1112/sshreader/commits/156c9a0f694816783cd1dd3f1904b9c3d7cbad4f)
 * Added warnings for exceeding threadlimit [808a5d4](https://bitbucket.org/isaiah1112/sshreader/commits/808a5d4558d84e0aa06a491d03da5ed6f20b27cd)
 * Adding documentation for getting started. [5ab175f](https://bitbucket.org/isaiah1112/sshreader/commits/5ab175f48df35dd9f60c3f5425de97431a82c50c)
 * Added envvars method which attempts to gather username and ssh_key info from OS. [6911582](https://bitbucket.org/isaiah1112/sshreader/commits/69115829d3d118c5b36ed9325d50e6f1eb66aa6e)

## Version 3.1
 * Using os and getpass modules in conjunction when determining username. [1199c86](https://bitbucket.org/isaiah1112/sshreader/commits/1199c8616cf6a3441dcc77fd2828971617fe4128)
 * Added decodebytes flag to ssh_command and shell_command for decoding byte-strings to unicode-strings. This can help with compatibility when using Python 3. [86a7ed0](https://bitbucket.org/isaiah1112/sshreader/commits/86a7ed01d9c069fea02b409d3892557d5fb2a23b)
 * Using all unicode_literals because, well, because I said so! [7c247e9](https://bitbucket.org/isaiah1112/sshreader/commits/7c247e9938eb9340bf9b1afc4975304a4b6d9832)
 * Added unicode strings FAQ. [3d76108](https://bitbucket.org/isaiah1112/sshreader/commits/3d761080b447203e8cbe544ea27c8c804c866bc3)
 * Added timeout flag to pydsh cli so it can be overriden for long running commands. [2999e5c](https://bitbucket.org/isaiah1112/sshreader/commits/2999e5c836eb1d33af4577c9fc9f9b45a9631be5)

# Version 3.0.1
 * Fixed typo in ssh docstring [328bb5c](https://bitbucket.org/isaiah1112/sshreader/commits/328bb5c86e6313d452e20406665f5a3e5507425c)
 * SSH class can now be used with Python 'with' statement [f54ac3d](https://bitbucket.org/isaiah1112/sshreader/commits/f54ac3d5fd342cbcfae2315f1be7043fe40d65a1)

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
