import importlib.util
import pkgutil
import sys
import os


def get_submodules(mod):
    submods = []
    for submod in pkgutil.iter_modules(mod.__path__):
        submods.append(submod.name)

    return submods


def lazy_import(name):
    spec = importlib.util.find_spec(name)
    loader = importlib.util.LazyLoader(spec.loader)
    spec.loader = loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    loader.exec_module(module)
    return module


def ensure_directory(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
