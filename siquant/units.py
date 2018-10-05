import numbers

from .dimensions import SIDimensions, dim_div, dim_mul, dim_pow, dim_str
from .quantities import ScalarQuantity


class SIUnit:
    __slots__ = ("_scale", "_dimensions")

    @staticmethod
    def Unit(scale=1.0, kg=0, m=0, s=0, k=0, a=0, mol=0, cd=0):
        return SIUnit(scale, SIDimensions(kg=kg, m=m, s=s, k=k, a=a, mol=mol, cd=cd))

    def __init__(self, scale, dimensions):
        if scale <= 0:
            raise ValueError("SIunit scale must be positive.")
        self._scale = scale
        self._dimensions = dimensions

    scale = property(lambda self: self._scale)
    dimensions = property(lambda self: self._dimensions)

    kg = property(lambda self: self._dimensions[0])
    m = property(lambda self: self._dimensions[1])
    s = property(lambda self: self._dimensions[2])
    k = property(lambda self: self._dimensions[3])
    a = property(lambda self: self._dimensions[4])
    mol = property(lambda self: self._dimensions[5])
    cd = property(lambda self: self._dimensions[6])

    def base_units(self):
        return SIUnit(1.0, self._dimensions)

    def compatible(self, units):
        return self._dimensions == units._dimensions

    def __mul__(self, other):
        if isinstance(other, SIUnit):
            return SIUnit(
                self._scale * other._scale, dim_mul(self._dimensions, other._dimensions)
            )
        if isinstance(other, numbers.Real):
            return ScalarQuantity(other, self)
        if isinstance(other, ScalarQuantity):
            return ScalarQuantity(other.get(), other.units * self)
        return NotImplemented

    def __imul__(self, other):
        if isinstance(other, SIUnit):
            return SIUnit(
                self._scale * other._scale, dim_mul(self._dimensions, other._dimensions)
            )
        return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, numbers.Real):
            return ScalarQuantity(other, self)
        if isinstance(other, ScalarQuantity):
            return ScalarQuantity(other.get(), other.units * self)
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, SIUnit):
            return SIUnit(
                self._scale / other._scale, dim_div(self._dimensions, other._dimensions)
            )
        if isinstance(other, numbers.Real):
            return ScalarQuantity(1 / other, self)
        if isinstance(other, ScalarQuantity):
            return ScalarQuantity(1 / other.get(), self / other.units)
        return NotImplemented

    __itruediv__ = __truediv__

    def __rtruediv__(self, other):
        if isinstance(other, numbers.Real):
            return ScalarQuantity(other, ~self)
        if isinstance(other, ScalarQuantity):
            return ScalarQuantity(other.get(), other.units / self)
        return NotImplemented

    def __pow__(self, exponent):
        if isinstance(exponent, numbers.Real):
            return SIUnit(self._scale ** exponent, dim_pow(self._dimensions, exponent))
        return NotImplemented

    def __invert__(self):
        return SIUnit(1 / self._scale, dim_div(SIDimensions(), self._dimensions))

    def __eq__(self, other):
        if isinstance(other, SIUnit):
            return self._scale == other._scale and self._dimensions == other._dimensions
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, SIUnit):
            return self._scale != other._scale or self._dimensions != other._dimensions
        return NotImplemented

    def __hash__(self):
        return hash((self._scale, self._dimensions))

    def __str__(self):
        return "%g*%s" % (self._scale, dim_str(self._dimensions))

    def __repr__(self):
        return "SIUnit(%f, %r)" % (self._scale, self._dimensions)
