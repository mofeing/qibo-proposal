import inspect
from typing import TypeVar


def check_methods(cls, *methods):
    return all(hasattr(cls, method) and inspect.ismethod(getattr(cls, method)) for method in methods)


T = TypeVar("T")


def Const(obj: T) -> T:
    def getter(_):
        return obj

    if hasattr(obj, "__del__"):

        def deletter(o):
            o.__del__()

    else:
        deletter = None

    return property(fget=getter, fset=None, fdel=deletter)
