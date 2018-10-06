from .exceptions import ImmutabilityError


def __si_immutable_setattr(inst, key, value):
    raise ImmutabilityError(inst, key)


def __si_immutable_delattr(inst, key):
    raise ImmutabilityError(inst, key)


def immutable(cls):
    cls.__setattr__ = __si_immutable_setattr
    cls.__delattr__ = __si_immutable_delattr
    return cls
