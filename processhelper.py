from multiprocessing.managers import BaseManager, NamespaceProxy

__author__ = 'Waner Miranda'
__email__ = 'waner@dcc.ufmg.br'


def join_process(process):
    for t in process:
        t.join()
    process = []
    return process


class SolverManager(BaseManager):
    pass


class SolverProxy(NamespaceProxy):
    _exposed_ = ('__getattribute__', '__setattr__', '__delattr__', 'evaluate')

    def evaluate(self, starting_pos, part, parts):
        callmethod = object.__getattribute__(self, '_callmethod')
        return callmethod(self.evaluate.__name__, (starting_pos, part, parts))


def evaluate(solver_proxy, part, parts):
    solver_proxy.evaluate(1, part, parts)
