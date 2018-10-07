import weakref

from .exceptions import ImmutabilityError


def __si_immutable_setattr(inst, key, value):
    raise ImmutabilityError(inst, key)


def __si_immutable_delattr(inst, key):
    raise ImmutabilityError(inst, key)


def immutable(cls):
    cls.__setattr__ = __si_immutable_setattr
    cls.__delattr__ = __si_immutable_delattr
    return cls


def flyweight(cls):
    instances = weakref.WeakValueDictionary()
    cls.__new__ = lambda cls, *args: instances.setdefault(args, object.__new__(cls))
    # def __new__(cls, *args):
    #    if not args in instances:
    #        new_instance = object.__new__(cls)
    #        instances[args] = new_instance
    #    return instances[args]
    # cls.__new__ = __new__
    return cls
