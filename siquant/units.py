from quantities import Quantity
from siquant.dimensions import Dimensions, dim_str, dim_pow, dim_mul, dim_div

class Unit:
    __slots__ = ('_scale', '_dimensions')

    @staticmethod
    def Unit(scale=1.0, kg=0, m=0, s=0, k=0, a=0, mol=0, cd=0):
        return Unit(scale, Dimensions(kg=kg, m=m, s=s, k=k, a=a, mol=mol, cd=cd))

    def __init__(self, scale, dimensions):
        self._scale = scale
        self._dimensions = dimensions

    scale = property(lambda self: self._scale)
    dimensions = property(lambda self: self._dims)

    def base_units(self):
        return Unit(1.0, self._dimensions)

    def __mul__(self, other):
        if isinstance(other, Unit):
            return Unit(
                self._scale * other._scale,
                dim_mul(self._dimensions, other._dimensions)
            )
        else:
            return Quantity(other, self)

    def __rmul__(self, other):
        return Quantity(other, self)

    def __truediv__(self, other):
        if isinstance(other, Unit):
            return Unit(
                self._scale / other._scale,
                dim_div(self._dimensions, other._dimensions)
            )
        else:
            return Quantity(1 / other, self)

    def __rtruediv__(self, other):
        return Quantity(other, self)

    def __pow__(self, exponent):
        return Unit(
            self._scale ** exponent,
            dim_pow(self._dimensions, exponent)
        )

    def __invert__(self):
        return Unit(
            1 / self._scale,
            dim_div(Dimensions(), self._dimensions)
        )

    def __eq__(self, other):
        if not isinstance(other, Unit):
            return NotImplemented
        return self._scale == other._scale and self._dimensions == other._dimensions

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return '%g*%s' % (self._scale, dim_str(self._dimensions))

    def __repr__(self):
        return 'Unit(%f, %r)' % (
            self._scale,
            self._dimensions
        )

