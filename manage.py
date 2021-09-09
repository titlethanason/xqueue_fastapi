from Util import nbmanager
import sys


def main(argv):
    if len(argv) == 2 and argv[0] == 'generate':
        assignment_id = argv[1]
        ret = nbmanager.generate(assignment_id)
        print(ret)
    else:
        print('usage: nbmanager.py generate <id>')


if __name__ == '__main__':
    main(sys.argv[1:])
