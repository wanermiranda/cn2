#!/bin/python
import aco
import errno, sys
import getopt


def usage():
    print 'example: main.py -f entrada.txt'
    sys.exit(0)


__author__ = 'Waner Miranda'


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

    aco.Solver(dataset_file)

if __name__ == "__main__":
    main()

