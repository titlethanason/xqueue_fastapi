import logging
from fastapi import FastAPI, Request, BackgroundTasks
from Controller import handler

app = FastAPI()

logging.basicConfig(filename="xqueue_fastapi.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
logging.info("Running xqueue_fastapi")


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
    # body = await request.body()
    # print(eval(body))
    bg.add_task(handler.process)
    return {"status": 1}
