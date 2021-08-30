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


def _grade(request):
    problem_number = eval(request["body"]["grader_payload"])["problem_number"]
    if problem_number == 1:
        file = request["file"]
        filename = list(file.values())[0].split("/")[-1]
        return problem1.process(filename)

    elif problem_number == 2:
        code = request["body"]["student_response"]
        return problem2.process(code)


def process():
    start = time.time()
    try:
        # get queue from xqueue
        outs = _get_queue()

        # eval output from tutor-xqueue
        res = _eval_request(outs)

        # process the queue detail
        result = _grade(res)
        score = str(result["score"])
        correct = str(result["correct"])
        msg = str(result["msg"])
        logging.info(f'Grading detail ({res["key"]}):')
        print(f'Success grading {res["key"]}')

        # response back to the tutor-xqueue
        _put_result(str(res["id"]), str(res["key"]), score, correct, msg)

        time_elapsed = time.time() - start
        logging.info(f'Process {res["key"]} use {time_elapsed} seconds')
        print(f'Time elapsed for {res["key"]}: {time_elapsed} seconds')

    except TimeoutExpired as err:
        logging.error(f'Timeout in proc.communicate(): {err}')
    except Exception as err:
        logging.error(f'{err}')
