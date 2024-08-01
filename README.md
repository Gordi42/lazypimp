# Lazypimp
Lazypimp stands for lazy python import. It is a python package that allows you to setup an importing system that loads all imports on demand. This is useful for large projects where you don't want to load all the imports at once.

## Installation
using pip:
```bash
pip install lazypimp
```

## Usage
Let's say we have a file structure as follows:
```
mymodule/
    __init__.py
    submod1.py
    submod2.py
    submod3.py
    subpackage/
        __init__.py
        submod4.py
    class1.py
    functions.py
```
And we want to have the following imports in the `__init__.py` file:
```python
# imports of submodules
from mymodule import submod1, submod2, submod3 as sm3
from mymodule.subpackage import submod4

# imports of classes, functions, etc.
from mymodule.class1 import MyClass1
from mymodule.functions import my_function
```

To set up the module `mymodule` to load submodules on demand, we can use the following code:
```python

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
```
