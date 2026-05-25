# encoding: utf-8

"""Currently unsupported and non-functional."""

raise ImportError("This module is currently unsupported.")


import transaction

from functools import partial

from zope.interface import implements
from transaction.interfaces import IDataManager
  
from marrow.mailer.manager.dynamic import ScalingPoolExecutor, DynamicManager


__all__ = ['TransactionalDynamicManager']

log = __import__('logging').getLogger(__name__)



class ExecutorDataManager(object):
    implements(IDataManager)
    
    __slots__ = ('callback', 'abort_callback')
    
    def __init__(self, callback, abort=None, pool=None):
        self.callback = callback
        self.abort_callback = abort
    
    def commit(self, transaction):
        pass
    
    
    
    def abort_sub(self, transaction):
        pass
    
    commit_sub = abort_sub
    
    def beforeCompletion(self, transaction):
        pass
    
    afterCompletion = beforeCompletion
    
    
    def tpc_vote(self, transaction):
        pass
    
    
    tpc_abort = abort


class TransactionalScalingPoolExecutor(ScalingPoolExecutor):
    
    
    def submit(self, fn, *args, **kwargs):
        with self._shutdown_lock:
            if self._shutdown:
                raise RuntimeError('cannot schedule new futures after shutdown')
            
            f = _base.Future()
            w = _WorkItem(f, fn, args, kwargs)
            
            dm = ExecutorDataManager(partial(self._submit, w), partial(self._cancel_tn, f))
            transaction.get().join(dm)
            
            return f


class TransactionalDynamicManager(DynamicManager):
    name = "Transactional dynamic"
    Executor = TransactionalScalingPoolExecutor
