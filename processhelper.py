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
    _exposed_ = ('__getattribute__', '__setattr__', '__delattr__', 'evaluate', 'prepare_iteration', 'get_best_path')

    def evaluate(self, starting_pos, part, parts):
        callmethod = object.__getattribute__(self, '_callmethod')
        return callmethod(self.evaluate.__name__, (starting_pos, part, parts))

def prepare_iteration(self):
        callmethod = object.__getattribute__(self, '_callmethod')
        return callmethod(self.evaluate.__name__, ())

def evaluate(solver_proxy, part, parts):
    solver_proxy.evaluate(part, parts, part)

def solver_callmethod(solver, name, args):
    callmethod = solver.__getattribute__('_callmethod')
    return callmethod(name, args)

def solver_getattribute(solver, name):
    return solver.__getattribute__(name)
