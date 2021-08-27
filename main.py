import logging
from subprocess import PIPE, Popen, TimeoutExpired
from fastapi import FastAPI, Request, BackgroundTasks
import time

app = FastAPI()

logging.basicConfig(filename="xqueue_fastapi.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
logging.info("Running xqueue_fastapi")


def get_submission():
    start = time.time()
    try:
        # get queue from xqueue
        proc = Popen(["tutor", "xqueue", "submissions", "show"], stdout=PIPE, stderr=PIPE)
        outs, errs = proc.communicate(timeout=10)
        if len(errs) != 0:
            raise Exception(f'Error fetching data from tutor-xqueue')
        logging.info(f'Queue detail: {outs.decode("utf-8")}')
        print(f'Success fetching')
        proc.kill()

        # eval output from tutor-xqueue
        try:
            res = eval(outs)  # convert from bytes-like to object in python
        except SyntaxError as err:
            raise Exception(f'Error eval output from tutor-xqueue: {err}')
        logging.info(f'Eval success ({res["key"]})')
        print(f'Success eval {res["key"]}')

        # process the queue detail
        point = str(1)
        is_true = str("true")
        msg = str("Good job!")
        logging.info(f'Grading detail ({res["key"]}):')
        print(f'Success grading {res["key"]}')

        # response back to the tutor-xqueue
        proc = Popen(["tutor", "xqueue", "submissions", "grade", str(res["id"]), res["key"], point, is_true, msg],
                     stdout=PIPE, stderr=PIPE)
        outs, errs = proc.communicate(timeout=10)
        if len(errs) != 0:
            raise Exception(f'Error put result of {res["key"]} in tutor-xqueue')
        time_elapsed = time.time() - start
        logging.info(f'Put result response ({res["key"]}): {outs.decode("utf-8")} using {time_elapsed} seconds')
        print(f'Time elapsed for {res["key"]}: {time_elapsed} seconds')
        proc.kill()

    except TimeoutExpired as err:
        logging.error(f'Timeout in proc.communicate(): {err}')
    except Exception as err:
        logging.error(f'{err}')


@app.get("/")
def read_root():
    return {"status": 1}


@app.post("/")
async def home(request: Request):
    body = await request.body()
    print(body.decode('utf-8'))
    return {"status": 1}


@app.post("/submit")
async def submit(request: Request, bg: BackgroundTasks):
    body = await request.body()
    print(eval(body))
    bg.add_task(get_submission)
    return {"status": 1}
