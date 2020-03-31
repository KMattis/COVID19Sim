import importlib.util
import inspect

def readNeedTypes(configFile):
    spec = importlib.util.spec_from_file_location("need_types", configFile)
    needTypesModule = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(needTypesModule)
    return [obj() for (_, obj) in inspect.getmembers(needTypesModule) if inspect.isclass(obj)]
