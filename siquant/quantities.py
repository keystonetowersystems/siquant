import numbers
from functools import total_ordering

from .exceptions import UnitMismatchError, unexpected_type_error
from .util import immutable


@immutable
class Quantity:
    __slots__ = ("quantity", "units")

    @classmethod
    def As(cls, units):
        def cvt(quantity):
            if isinstance(quantity, cls):
                return quantity.cvt_to(units)
            return cls(quantity, units)

        return cvt

    def __init__(self, quantity, units):
        super().__setattr__("quantity", quantity)
        super().__setattr__("units", units)

    def is_of(self, dimensions):
        return self.units.dimensions == dimensions

    def get_as(self, units):
        if not self.units.compatible(units):
            raise UnitMismatchError(self.units, units)
        return self.units.scale / units.scale * self.quantity

    def cvt_to(self, units):
        return self.__class__(self.get_as(units), units)

    def compatible(self, other):
        if not isinstance(other, Quantity):
            raise unexpected_type_error("other", Quantity, other)
        return self.units.compatible(other.units)

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(self.quantity + other.get_as(self.units), self.units)
        return NotImplemented

    __iadd__ = __add__

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(self.quantity - other.get_as(self.units), self.units)
        return NotImplemented

    __isub__ = __sub__

    def __neg__(self):
        return self.__class__(-self.quantity, self.units)

    def __bool__(self):
        return bool(self.quantity)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.units.compatible(other.units) and self.quantity == other.get_as(
                self.units
            )
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, type(self)):
            return not self.units.compatible(
                other.units
            ) or self.quantity != other.get_as(self.units)
        return NotImplemented

    def __hash__(self):
        return hash((self.quantity * self.units.scale, self.units.base_units()))

    def __str__(self):
        return "%s %s" % (self.quantity, self.units)

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self.quantity, self.units)


@immutable
@total_ordering
class ScalarQuantity(Quantity):
    __slots__ = ()

    def __abs__(self):
        return ScalarQuantity(abs(self.quantity), self.units)

    def __lt__(self, other):
        if isinstance(other, ScalarQuantity):
            return self.quantity < other.get_as(self.units)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, ScalarQuantity):
            return ScalarQuantity(
                self.quantity * other.quantity, self.units * other.units
            )
        if isinstance(other, numbers.Real):
            return ScalarQuantity(self.quantity * other, self.units)
        return NotImplemented

    __imul__ = __mul__

    def __rmul__(self, other):
        if isinstance(other, numbers.Real):
            return ScalarQuantity(other * self.quantity, self.units)
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, ScalarQuantity):
            return ScalarQuantity(
                self.quantity / other.quantity, self.units / other.units
            )
        if isinstance(other, numbers.Real):
            return ScalarQuantity(self.quantity / other, self.units)
        return NotImplemented

    __itruediv__ = __truediv__

    def __rtruediv__(self, other):
        if isinstance(other, numbers.Real):
            return ScalarQuantity(other / self.quantity, ~self.units)
        return NotImplemented

    def __pow__(self, exponent):
        if isinstance(exponent, numbers.Real):
            return ScalarQuantity(self.quantity ** exponent, self.units ** exponent)
        return NotImplemented

    def __invert__(self):
        return ScalarQuantity(1 / self.quantity, ~self.units)
