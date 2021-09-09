from Util import filemanager
import logging


def process(filename):
    module = filemanager.load_module(filename, "hello")
    try:
        result = module.squared(10)
        print(f'Result from uploaded file: {result}')
        return {"correct": True, "score": 1, "msg": f'Correct !! (result of 10 squared is {result})'}
    except (ValueError, AttributeError) as err:
        print(f'Error at calling function in uploaded file: {err}')
        raise Exception(f'Error at calling function in uploaded file: {err}')
