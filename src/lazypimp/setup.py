import sys
from types import ModuleType
import importlib


def setup(module_name, all_modules_by_origin, all_imports_by_origin):
    """
    Set up a module to load submodules on demand.
    
    Description
    -----------
    This function sets up a module to load imports and submodules on demand.
    All submodules should be listed in the `all_modules_by_origin` dictionary.
    All imports should be listed in the `all_imports_by_origin` dictionary.
    More information on how to use this function can be found on GitHub:
    https://github.com/Gordi42/lazypimp
    
    Parameters
    ----------
    `module_name` : `str`
        The name of the module that should be set up, typically `__name__`.
    `all_modules_by_origin` : `dict`
        A dictionary that maps module names to their origin (see example).
    `all_imports_by_origin` : `dict`
        A dictionary that maps import names to their origin (see example).
    
    Examples
    --------
    Let's say we have a module `mymodule` that has the following imports:
    in the `__init__.py` file:

    .. code-block:: python

        # imports of submodules
        from mymodule import submod1, submod2, submod3 as sm3
        from mymodule.subpackage import submod4

        # imports of classes, functions, etc.
        from mymodule.class1 import MyClass1
        from mymodule.functions import my_function
    
    We can set up the module `mymodule` to load submodules on demand as follows:

    .. code-block:: python

        from lazypimp import setup

        all_modules_by_origin = {
            "mymodule": ["submod1", "submod2", {"sm3": "submod3"}], 
            "mymodule.subpackage": ["submod4"]
        }

        all_imports_by_origin = {
            "mymodule.class1": "MyClass1",
            "mymodule.functions": "my_function"
        }

        setup(__name__, all_modules_by_origin, all_imports_by_origin)

    """
    # Set up dictionary that maps an import to a path
    # items in the all_modules_by_origin dictionary are imported as modules
    origins = {}
    all_modules = []
    for origin, items in all_modules_by_origin.items():
        for item in items:
            if isinstance(item, dict):
                alias, item = list(item.items())[0]
            else:
                alias = item
            all_modules.append(alias)
            origins[alias] = origin + "." + item

    # items in the all_imports_by_origin dictionary are imported as elements of a module
    imports = {}
    all_imports = []
    for origin, items in all_imports_by_origin.items():
        for item in items:
            if isinstance(item, dict):
                alias, item = list(item.items())[0]
            else:
                alias = item
            all_imports.append(alias)
            origins[alias] = origin
            imports[alias] = item

    # load submodules on demand
    class Module(ModuleType):
        def __getattr__(self, name):
            if name not in all_modules + all_imports:
                raise AttributeError(
                        f"module {__name__!r} has no attribute {name!r}")

            mod = importlib.import_module(origins[name])
            # check if the attribute is an import
            if name in all_imports:
                mod = getattr(mod, imports[name])
            # set the attribute in the current module such that it is not loaded again
            setattr(self, name, mod)
            # return the attribute
            return mod

    sys.modules[module_name].__class__ = Module
    sys.modules[module_name].__all__ = all_modules + all_imports
