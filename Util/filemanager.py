import importlib.util
import settings


def load_module(filename, name="problem_module"):
    spec = importlib.util.spec_from_file_location(name, settings.SAVE_FILE_PATH+filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def save_file(code=None):
    return settings.SAVE_FILE_PATH
