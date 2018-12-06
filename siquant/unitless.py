from abc import ABC


class Unitless(ABC):
    pass


Unitless.register(float)
Unitless.register(int)
