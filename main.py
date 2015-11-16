#!/bin/python
import multiprocessing
import aco
import processhelper as ph
import errno, sys
import getopt

__author__ = 'Waner Miranda'
__email__ = 'waner@dcc.ufmg.br'

MAX_ITERATIONS = 2500


def usage():
    print 'example: main.py -f input.txt'
    sys.exit(0)


def main():
    anthill_size = 100
    evaporation_rate = 0.3
    dataset_file = 'entrada2.txt'
    try:
        arg_list = sys.argv[1:]
        opts, args = getopt.getopt(arg_list, 'f:a:e:h', ['dataset_file=', 'anthill_size', 'evaporation_rate=' 'help'])
    except getopt.GetoptError:
        usage()
        raise
    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt in ("-f", "--dataset_file"):
            dataset_file = arg
        elif opt in ("-e", "--evaporation_rate"):
            evaporation_rate = float(arg)
        elif opt in ("-a", "--anthill_size"):
            anthill_size = int(arg)

    ph.SolverManager.register('Solver', aco.Solver, ph.SolverProxy)
    manager = ph.SolverManager()
    manager.start()
    print dataset_file, anthill_size, evaporation_rate
    solver = manager.Solver(dataset_file, anthill_size, evaporation_rate)

    for i in range(MAX_ITERATIONS):

        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        parts = 5
        for part in range(1, parts):
            # print 'Apply', part
            pool.apply_async(func=ph.evaluate, args=(solver, part, parts - 1))

        pool.close()
        pool.join()
        ph.solver_callmethod(solver, 'prepare_iteration', ())
        best_solution = ph.solver_callmethod(solver, 'get_best_path', ())
        print 'Iter:', i, best_solution[1]

if __name__ == "__main__":
    main()
