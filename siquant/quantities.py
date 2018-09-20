import numbers
from functools import total_ordering

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
        assert (self._units.compatible(units))
        return self._units._scale / units._scale * self._quantity

    def cvt_to(self, units):
        return self.__class__(self.get_as(units), units)

    def normalized(self):
        return self.__class__(self._quantity / self._units._scale, self._units.base_units())

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(self._quantity + other.get_as(self._units), self._units)
        return NotImplemented

    __iadd__ = __add__

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(self._quantity - other.get_as(self._units), self._units)
        return NotImplemented

    __isub__ = __sub__

    def __neg__(self):
        return self.__class__(-self._quantity, self._units)


    def __bool__(self):
        return bool(self._quantity)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self._units.compatible(other._units) and self._quantity == other.get_as(self._units)
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, type(self)):
            return not self._units.compatible(other._units) or self._quantity != other.get_as(self._units)
        return NotImplemented

    def __str__(self):
        return '%s %s' % (self._quantity, self._units)

    def __repr__(self):
        return '%s(%r, %r)' % (self.__class__.__name__, self._quantity, self._units)

@total_ordering
class ScalarQuantity(Quantity):
    __slots__ = ()

    def __abs__(self):
        return ScalarQuantity(abs(self._quantity), self._units)

    def __lt__(self, other):
        if isinstance(other, ScalarQuantity):
            return self._units.compatible(other._units) and self._quantity < other.get_as(self._units)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, ScalarQuantity):
            return ScalarQuantity(self._quantity * other._quantity, self._units * other._units)
        if isinstance(other, numbers.Real):
            return ScalarQuantity(self._quantity * other, self._units)
        return NotImplemented

    __imul__ = __mul__

    def __rmul__(self, other):
        if isinstance(other, numbers.Real):
            return ScalarQuantity(other * self._quantity, self._units)
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, ScalarQuantity):
            return ScalarQuantity(self._quantity / other._quantity, self._units / other._units)
        if isinstance(other, numbers.Real):
            return ScalarQuantity(self._quantity / other, self._units)
        return NotImplemented

    __itruediv__ = __truediv__

    def __rtruediv__(self, other):
        if isinstance(other, numbers.Real):
            return ScalarQuantity(other / self._quantity, ~self._units)
        return NotImplemented

    def __pow__(self, exponent):
        if isinstance(exponent, numbers.Real):
            return ScalarQuantity(self._quantity ** exponent, self._units ** exponent)
        return NotImplemented

    def __invert__(self):
        return ScalarQuantity(1 / self._quantity, ~self._units)
