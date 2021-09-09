from Util import nbmanager
import logging


def process(filename, assignment_id="test001", problem_id="test001_1"):
    try:
        ret = nbmanager.grade(filename, assignment_id, problem_id)
        final_score = ret["score"]/ret["max_score"]
        return {"correct": True, "score": final_score, "msg": f'You got {ret["score"]} out of {ret["max_score"]}'}
    except Exception as err:
        print(f'Error at grading notebook {assignment_id} at {filename}: {err}')
        raise Exception(f'Error at grading notebook {assignment_id} at {filename}: {err}')
