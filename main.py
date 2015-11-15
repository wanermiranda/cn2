#!/bin/python
import multiprocessing
import aco
import processhelper as ph
import errno, sys
import getopt

__author__ = 'Waner Miranda'
__email__ = 'waner@dcc.ufmg.br'


def usage():
    print 'example: main.py -f input.txt'
    sys.exit(0)


def main():
    try:
        arg_list = sys.argv[1:]
        opts, args = getopt.getopt(arg_list, 'f:h', ['dataset_file=', 'help'])
    except getopt.GetoptError:
        usage()
        raise
    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt in ("-f", "--dataset_file"):
            dataset_file = arg

    ph.SolverManager.register('Solver', aco.Solver, ph.SolverProxy)
    manager = ph.SolverManager()
    manager.start()
    solver = manager.Solver(dataset_file)
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    parts = 4
    for iteration in range(100):
        for part in range(1, parts):
            pool.apply(func=ph.evaluate, args=(solver, part, parts))


if __name__ == "__main__":
    main()
