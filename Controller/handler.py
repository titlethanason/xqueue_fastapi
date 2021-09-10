from Problem import *
import time
import logging
from subprocess import PIPE, Popen, TimeoutExpired


def _get_queue():
    proc = Popen(["tutor", "xqueue", "submissions", "show"], stdout=PIPE, stderr=PIPE)
    outs, errs = proc.communicate(timeout=10)
    if len(errs) != 0:
        raise Exception(f'Error fetching data from tutor-xqueue')
    logging.info(f'Queue detail: {outs.decode("utf-8")}')
    proc.kill()
    print(f'Success fetching')
    return outs


def _eval_request(outs):
    try:
        res = eval(outs)  # convert from bytes-like to object in python
    except SyntaxError as err:
        raise Exception(f'Error eval output from tutor-xqueue: {err}')
    logging.info(f'Eval success ({res["key"]})')
    print(f'Success eval {res["key"]}')
    return res


def _put_result(request_id, request_key, score, correct, msg):
    proc = Popen(["tutor", "xqueue", "submissions", "grade", request_id, request_key, score, correct, msg],
                 stdout=PIPE, stderr=PIPE)
    outs, errs = proc.communicate(timeout=10)
    if len(errs) != 0:
        raise Exception(f'Error put result of {request_key} in tutor-xqueue')
    logging.info(f'Put result response ({request_key}): {outs.decode("utf-8")}')
    proc.kill()
    print(f'Success put_result {request_key}')


def _grade(req):
    problem_number = eval(req["body"]["grader_payload"])["problem_number"]
    if problem_number == 1:
        file = req["file"]
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
        outs = _get_queue()

        # eval output from tutor-xqueue
        req = _eval_request(outs)

        # process the queue detail
        result = _grade(req)
        score = str(result["score"])
        correct = str(result["correct"])
        msg = str(result["msg"])
        logging.info(f'Grading detail ({req["key"]}): {result}')
        print(f'Success grading {req["key"]}')

        # response back to the tutor-xqueue
        _put_result(str(req["id"]), str(req["key"]), score, correct, msg)

        time_elapsed = time.time() - start
        logging.info(f'Process {req["key"]} use {time_elapsed} seconds')
        print(f'Time elapsed for {req["key"]}: {time_elapsed} seconds')

    except TimeoutExpired as err:
        logging.error(f'Timeout in proc.communicate(): {err}')
    except Exception as err:
        logging.error(f'{err}')
