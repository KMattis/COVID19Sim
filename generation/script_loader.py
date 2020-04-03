import importlib.util
import inspect

def readObjectsFromScript(configFile, name):
    spec = importlib.util.spec_from_file_location(name, configFile)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return [obj() for (_, obj) in inspect.getmembers(module) if inspect.isclass(obj)]
