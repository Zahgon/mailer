# encoding: utf-8

import atexit
import threading
import weakref
import sys
import math

from functools import partial

from marrow.mailer.manager.futures import worker
from marrow.mailer.manager.util import TransportPool

try:
    import queue
except ImportError:
    import Queue as queue

try:
    from concurrent import futures
except ImportError:  # pragma: no cover
    raise ImportError("You must install the futures package to use background delivery.")


__all__ = ['DynamicManager']

log = __import__('logging').getLogger(__name__)




class WorkItem(object):
    __slots__ = ('future', 'fn', 'args', 'kwargs')

    def __init__(self, future, fn, args, kwargs):
        self.future = future
        self.fn = fn
        self.args = args
        self.kwargs = kwargs



class ScalingPoolExecutor(futures.ThreadPoolExecutor):
    def __init__(self, workers, divisor, timeout):
        self._max_workers = workers
        self.divisor = divisor
        self.timeout = timeout

        self._work_queue = queue.Queue()

        self._threads = set()
        self._shutdown = False
        self._shutdown_lock = threading.Lock()
        self._management_lock = threading.Lock()

        atexit.register(self._atexit)







class DynamicManager(object):
    __slots__ = ('workers', 'divisor', 'timeout', 'executor', 'transport')

    name = "Dynamic"
    Executor = ScalingPoolExecutor

    def __init__(self, config, transport):
        self.workers = int(config.get('workers', 10))  # Maximum number of threads to create.
        self.divisor = int(config.get('divisor', 10))  # Estimate the number of required threads by dividing the queue size by this.
        self.timeout = float(config.get('timeout', 60))  # Seconds before starvation.

        self.executor = None
        self.transport = TransportPool(transport)

        super(DynamicManager, self).__init__()


    def deliver(self, message):
        # Return the Future object so the application can register callbacks.
        # We pass the message so the executor can do what it needs to to make
        # the message thread-local.
        return self.executor.submit(partial(worker, self.transport), message)

