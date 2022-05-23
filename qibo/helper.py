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


class hybridmethod:
    def __init__(self, fclassmethod=None, finstancemethod=None, doc=None):
        self.fclassmethod = fclassmethod
        self.finstancemethod = finstancemethod
        self.__doc__ = doc or self.fclassmethod.__doc__

    def classmethod(self, fclassmethod):
        return type(self)(fclassmethod, self.finstancemethod, None)

    def instancemethod(self, finstancemethod):
        return type(self)(self.fclassmethod, finstancemethod, self.__doc__)

    def __get__(self, instance, cls):
        if instance is None or self.finstancemethod is None:
            return self.fclassmethod.__get__(cls, None)
        return self.finstancemethod.__get__(instance, cls)
