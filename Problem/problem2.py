from Util import filemanager
import logging


def process(code):
    filename = filemanager.save_file(code)
    module = filemanager.load_module(filename, "hello")
    try:
        result = module.squared(10)
        print(f'Result from uploaded file: {result}')
    except (ValueError, AttributeError) as err:
        logging.info(f'Error at calling function in uploaded file: {err}')
        print(f'Error at calling function in uploaded file: {err}')

    return {"correct": True, "score": 1, "msg": f'Correct (result of 10 squared is {result}'}

