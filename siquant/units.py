import numbers

from .dimensions import SIDimensions, dim_div, dim_mul, dim_pow, dim_str
from .quantities import ScalarQuantity
from .util import immutable, flyweight


@flyweight
@immutable
class SIUnit:
    __slots__ = ("scale", "dimensions", "__weakref__")

    @staticmethod
    def Unit(scale=1.0, kg=0, m=0, s=0, k=0, a=0, mol=0, cd=0):
        return SIUnit(scale, SIDimensions(kg=kg, m=m, s=s, k=k, a=a, mol=mol, cd=cd))

    def __init__(self, scale, dimensions):
        if scale <= 0:
            raise ValueError("SIunit scale must be positive.")
        super().__setattr__("scale", scale)
        super().__setattr__("dimensions", dimensions)

    kg = property(lambda self: self.dimensions[0])
    m = property(lambda self: self.dimensions[1])
    s = property(lambda self: self.dimensions[2])
    k = property(lambda self: self.dimensions[3])
    a = property(lambda self: self.dimensions[4])
    mol = property(lambda self: self.dimensions[5])
    cd = property(lambda self: self.dimensions[6])

    def base_units(self):
        return SIUnit(1.0, self.dimensions)

    def compatible(self, units):
        return self.dimensions == units.dimensions

    def __mul__(self, other):
        if isinstance(other, SIUnit):
            return SIUnit(
                self.scale * other.scale, dim_mul(self.dimensions, other.dimensions)
            )
        if isinstance(other, numbers.Real):
            return ScalarQuantity(other, self)
        if isinstance(other, ScalarQuantity):
            return ScalarQuantity(other.quantity, other.units * self)
        return NotImplemented

    def __imul__(self, other):
        if isinstance(other, SIUnit):
            return SIUnit(
                self.scale * other.scale, dim_mul(self.dimensions, other.dimensions)
            )
        return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, numbers.Real):
            return ScalarQuantity(other, self)
        if isinstance(other, ScalarQuantity):
            return ScalarQuantity(other.quantity, other.units * self)
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, SIUnit):
            return SIUnit(
                self.scale / other.scale, dim_div(self.dimensions, other.dimensions)
            )
        if isinstance(other, numbers.Real):
            return ScalarQuantity(1 / other, self)
        if isinstance(other, ScalarQuantity):
            return ScalarQuantity(1 / other.quantity, self / other.units)
        return NotImplemented

    __itruediv__ = __truediv__

    def __rtruediv__(self, other):
        if isinstance(other, numbers.Real):
            return ScalarQuantity(other, ~self)
        if isinstance(other, ScalarQuantity):
            return ScalarQuantity(other.quantity, other.units / self)
        return NotImplemented

    def __pow__(self, exponent):
        if isinstance(exponent, numbers.Real):
            return SIUnit(self.scale ** exponent, dim_pow(self.dimensions, exponent))
        return NotImplemented

    def __invert__(self):
        return SIUnit(1 / self.scale, dim_div(SIDimensions(), self.dimensions))

    def __eq__(self, other):
        if isinstance(other, SIUnit):
            return self.scale == other.scale and self.dimensions == other.dimensions
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, SIUnit):
            return self.scale != other.scale or self.dimensions != other.dimensions
        return NotImplemented

    def __hash__(self):
        return hash((self.scale, self.dimensions))

    def __str__(self):
        return "%g*%s" % (self.scale, dim_str(self.dimensions))

    def __repr__(self):
        return "SIUnit(%f, %r)" % (self.scale, self.dimensions)
