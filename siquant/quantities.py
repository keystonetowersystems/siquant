
from functools import total_ordering

@total_ordering
class Quantity:
    __slots__ = ('_quantity', '_units')

    quantity = property(lambda self: self._quantity)
    units = property(lambda self: self._units)

    def __init__(self, quantity, units):
        self._quantity = quantity
        self._units = units

    def get(self):
        return self._quantity

    def get_as(self, units):
        assert(self._units.compatible(units))
        return self._quantity * self._units._scale / units._scale

    def cvt_to(self, units):
        return Quantity(self.get_as(units), units)

    def normalized(self):
        return Quantity(self._quantity / self._units._scale, self._units.base_units())

    def __eq__(self, other):
        if not isinstance(other, Quantity):
            return NotImplemented
        return self._units.compatible(other._units) and self._quantity == other.get_as(self._units)

    def __lt__(self, other):
        if not isinstance(other, Quantity):
            return NotImplemented
        return self._units.compatible(other._units) and self._quantity < other.get_as(self._units)

    def __add__(self, other):
        assert(self._units.compatible(other._units))
        return Quantity(self._quantity + other.get_as(self._units), self._units)

    __iadd__ = __add__

    def __sub__(self, other):
        assert(self._units.compatible(other._units))
        return Quantity(self._quantity - other.get_as(self._units), self._units)

    __isub__ = __sub__

    def __mul__(self, other):
        if isinstance(other, Quantity):
            return Quantity(self._quantity * other._quantity, self._units * other._units)
        return Quantity(other * self._quantity, self._units)

    __imul__ = __mul__

    def __rmul__(self, other):
        return Quantity(other * self._quantity, self._units)

    def __truediv__(self, other):
        if isinstance(other, Quantity):
            return Quantity(self._quantity / other._quantity, self._units / other._units)
        return Quantity(self._quantity / other, self._units)

    __itruediv__ = __truediv__

    def __rtruediv__(self, other):
        return Quantity(other / self._quantity, self._units)

    def __pow__(self, exponent):
        return Quantity(self._quantity ** exponent, self._units ** exponent)

    def __neg__(self):
        return Quantity(-self._quantity, self._units)

    def __abs__(self):
        return Quantity(abs(self._quantity), self._units)

    def __bool__(self):
        return bool(self._quantity)

    def __repr__(self):
        return '%s(%f, %r)' % (self.__class__.__name__, self._quantity, self._units)

