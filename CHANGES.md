# Changelog

# Version 2.3
 * Importing \_\_future__ statements for **print_function** and **division**
 * Moved into Python Package
 * Split SSH and **do_shell_script** into new ssh sub-module (called 'ssh')
 * Rebuilt Sphinx Documentation (and cleanded up docstrings)
 * Fixed bug with **ssh_command** function when combining *stderr* and *stdout*
 * Fixed bug when path to *keyfile* was relative to `~`

# Version 2.2.1
 * Publishing as Open Source (Thank you to [Level 3 Communications](http://www.level3.com) for giving me the approval to do this!)

# Version 2.2
 * Updated *pre* and *post* hooks to dictionaries as data structure
 * Added **tprint** function for attempt at thread-safe printing

# Version 2.1.4
 * Fixed bug with Paramiko log file warnings

# Version 2.1.2
 * Using **xrange** in Python2 to speed calculation
 * Attempting to fix bug when SSH session exits dirty, causing thread to hang
 * Updating tcp transport window size for Paramiko (per https://github.com/Paramiko/Paramiko/issues/175)

# Version 2.1
 * Imposing limits on number of **serverjobs** and sub-processes so you don't make a system unusable
 * Added ability to set *pcount* to -1 for maximum performance mode
 * Fixed bug when **sshread** method is called multiple times with *progressbar* enabled

# Version 2.0
 * **SSHreader** supports both multi-threading and multi-processing or a combination of both

# Version 1.6
 * Fixed bugs with *pre* and *post* hook statuses
 * Fixed bug if **serverjob** command is not in list form
 * Fixed bug when using SSH key with custom username
 * **Progress_bar** now only updates when percentage changes
 * Increased verbosity with *debuglevel* > 2
 * Changed to multiprocessing instead of threads

# Version 1.5
 * Improved individual SSH command statuses
 * Added ability for sshread method to accept single job (in non-list form)
 * Added ability to combine *stdout* and *stderr* from commands
 * Added Queues to manage **serverjob** object for threads (FINALLY)

# Version 1.4.3
 * Fixed bug where **progress_bar** was printed with every loop
 * Fixed bug where Paramiko was searching for SSH host keys
 * Fixed bug where Paramiko was search user SSH keys (we require a manually specified key location)
 * Added shorter-style progress bar

# Version 1.4
 * Added *progressbar* support during job processing
 * Added *pre* and *post* hooks for threads
 * SSH results now returned as tuple
 * Added ability to reconnect to a closed SSH connection
 * Added **is_alive** method for SSH connections

# Version 1.3
 * Added support for spawning non-threaded SSH sessions
 * Added support for running local shell commands (**do_shell_script** function)

# Version 1.2
 * Added support for limiting number of threads to spawn

# Version 1.1
 * Fixed bug when specifying username/password for SSH
 * Added debug levels for **sshreader**
 * Added more exception handling
 * Fixed bug with thread status

# Version 1.0
 * Initial Version of **sshreader**
 * Very simple threading and control of threads
