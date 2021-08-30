import importlib.util
import settings
import secrets


def load_module(filename, name="problem_module"):
    spec = importlib.util.spec_from_file_location(name, settings.SAVE_FILE_PATH+filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def save_file(code, extension='py'):
    filename = secrets.token_hex(16) + f'.{extension}'
    path = settings.SAVE_FILE_PATH + filename
    with open(path, 'w') as f:
        f.write(code)
    return filename
