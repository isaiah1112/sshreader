.. faq documentation master file, created by Jesse Almanrode

FAQ
===

Find answers to the frequently answered questions here.

Why are my print statements funky?
----------------------------------

Often times with multiprocessing print statements come out funky because multiple processes are writing to :code:`sys.stdout`.
One of the ways you can deal with this is by implementing a `multiprocessing.Lock()`_.  An example of how to use the
lock in a pre or post hook is shown below:

.. code-block:: python

    from multiprocessing import Lock
    # Make the Lock object global so all child processes can use it
    _print_lock_ = Lock()

    def my_hook(*args):
        """ Process safe print for pre/post hook

        :param args: Tuple of ( *args, <ServerJob> )
        :return: None
        """
        global _print_lock_
        thisjob = list(args).pop()
        with _print_lock_:
            print(str(thisjob.name))
        return None

Indices and tables
------------------

* :ref:`sshreader`
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
* `JA Computing`_

.. _JA Computing: http://www.jacomputing.net
.. _pdsh: https://computing.llnl.gov/linux/pdsh.html
.. _hostlist expressions: https://www.nsc.liu.se/~kent/python-hostlist/
.. _multiprocessing.Lock(): https://docs.python.org/2/library/multiprocessing.html#synchronization-between-processes
