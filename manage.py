from Util import nbmanager
import sys


def main(argv):
    if len(argv) == 2 and argv[0] == 'generate':
        assignment_id = argv[1]
        ret = nbmanager.generate(assignment_id)
        print(ret)
    elif len(argv) == 3 and argv[0] == 'autograde':
        assignment_id = argv[1]
        user_id = argv[2]
        ret = nbmanager.autograde(assignment_id, user_id)
        print(ret)
    elif len(argv) == 3 and argv[0] == 'get_submission':
        assignment_id = argv[1]
        user_id = argv[2]
        ret = nbmanager.get_submission(assignment_id, user_id)
        print(ret)
    else:
        print('usage: nbmanager.py generate <assignment_id>')
        print('       nbmanager.py autograde <assignment_id> <user_id>')
        print('       nbmanager.py get_submission <assignment_id> <user_id>')


if __name__ == '__main__':
    main(sys.argv[1:])
