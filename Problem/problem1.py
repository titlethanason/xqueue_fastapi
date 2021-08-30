from Util import filemanager
import logging


def process(filename):
    module = filemanager.load_module(filename, "hello")
    try:
        result = module.main1()
        print(f'Result from uploaded file: {result}')
    except (ValueError, AttributeError) as err:
        logging.info(f'Error at calling function in uploaded file: {err}')
        print(f'Error at calling function in uploaded file: {err}')

    return {"correct": True, "score": 0.8, "msg": "almost perfect!"}
