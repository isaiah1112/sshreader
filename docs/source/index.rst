.. _sshreader:

sshreader
=========

SSHreader is a Python library for running commands on multiple hosts in parallel. It wraps Paramiko and provides a direct SSH client, a job-based interface for parallel SSH and local commands, SFTP transfers, and the :code:`pydsh` command-line tool.

Use :class:`sshreader.ssh.SSH` to manage an individual SSH connection. For parallel work, create :class:`sshreader.utils.ServerJob` objects and pass a list of them to :func:`sshreader.utils.sshread`. Each job can run multiple commands sequentially on one host.

Jobs can be run with threads, processes, or both. When using multiprocessing, protect the program entry point with :code:`if __name__ == "__main__":`, as required by Python's spawn process model.

Topics
------

.. toctree::
   :maxdepth: 1

   getting_started
   faq
   pydsh
   testing

API Documentation
-----------------

.. toctree::
   :maxdepth: 1

   sshreader
   ssh

Compatibility
-------------

SSHreader requires Python 3.11 or later and declares support for Python versions below 4.0. The project currently tests Python 3.11 through 3.15.

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
