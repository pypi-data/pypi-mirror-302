# -*- coding: utf-8 -*-
#
# Author: GavinGong aka VisualDust
# Github: github.com/visualDust
# Date:   20230416


def singleton(class_):
    class class_w(class_):
        _instance = None

        def __new__(cls, *args, **kwargs):
            if class_w._instance is None:
                class_w._instance = super(class_w, cls).__new__(cls, *args, **kwargs)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def patch(func):
    """Patch a function into a class type

    Args:
        func (Function): A function that takes at least one argument with a specific class type 'self:YourClass'

    Returns:
        function: patched function
    """
    cls = next(iter(func.__annotations__.values()))
    defaults = func.__defaults__ or ()
    name = defaults[0] if defaults else None
    func.__qualname__ = f"{cls.__name__}.{func.__name__}"
    func.__module__ = cls.__module__
    if name is None:
        setattr(cls, func.__name__, func)
    else:
        func.__qualname__ = f"{cls.__name__}.{name}"
        setattr(cls, name, func)
    return func
