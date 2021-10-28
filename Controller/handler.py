from Problem import *
import time
import logging
import settings
from Util import tutor_interface


def _get_queue():
    print(settings.tutor_config)
    res = tutor_interface.get_xqueue_response(settings.tutor_config, "show_submission")
    if res["return_code"] != 0:
        raise Exception(f'Error fetching data from xqueue')
    logging.info(f'Queue detail: {res}')
    return res


def _put_result(request_id, request_key, score, correct, msg):
    res = tutor_interface.get_xqueue_response(settings.tutor_config, "grade_submission", request_id, request_key, score,
                                              correct, msg)
    if res["return_code"] != 0:
        raise Exception(f'Error put result of {request_key} in tutor-xqueue')
    logging.info(f'Put result response ({request_key}): {res}')
    print(f'Success put_result {request_key}')


def _grade(req):
    problem_number = eval(req["body"]["grader_payload"])["problem_number"]
    if problem_number == 1:
        file = req["files"]
        filename = list(file.values())[0].split("/")[-1]
        return problem1.process(filename)

    elif problem_number == 2:
        code = req["body"]["student_response"]
        return problem2.process(code)

    elif problem_number == 3:
        file = req["files"]
        filename = list(file.values())[0].split("/")[-1]
        payload = eval(req["body"]["grader_payload"])
        return problem3.process(filename, payload["assignment_id"], payload["problem_id"])


def process():
    start = time.time()
    try:
        # get queue from xqueue
        req = _get_queue()

        # process the queue detail
        result = _grade(req)
        logging.info(f'Grading detail ({req["key"]}): {result}')
        print(f'Success grading {req["key"]}')

        # response back to xqueue
        _put_result(str(req["id"]), str(req["key"]), result["score"], result["correct"], result["msg"])

        time_elapsed = time.time() - start
        logging.info(f'Process {req["key"]} use {time_elapsed} seconds')
        print(f'Time elapsed for {req["key"]}: {time_elapsed} seconds')

    except Exception as err:
        logging.error(f'{err}')
