import numbers
from functools import total_ordering

from .exceptions import UnitMismatchError, unexpected_type_error
from .util import immutable


def make(quantity, units):
    return units.factory(quantity, units)


def converter(units):
    def _converter(value):
        if isinstance(value, Quantity):
            return value.cvt_to(units)
        return make(value, units)

    return _converter


def is_of(dimensions):
    def _validator(value):
        if not isinstance(value, Quantity):
            return False
        return value.is_of(dimensions)

    return _validator


@immutable
@total_ordering
class Quantity:
    __slots__ = ("quantity", "units")

    def __init__(self, quantity, units):
        if isinstance(quantity, Quantity):
            units = quantity.units * units
            quantity = quantity.quantity
        super().__setattr__("quantity", quantity)
        super().__setattr__("units", units)

    def is_of(self, dimensions):
        return self.units.dimensions == dimensions

    def get_as(self, units):
        if self.units == units:
            return self.quantity
        if not self.units.compatible(units):
            raise UnitMismatchError(self.units, units)
        return self.units.scale / units.scale * self.quantity

    def cvt_to(quantity, units):
        return make(quantity.get_as(units), units)

    def compatible(self, other):
        if not isinstance(other, Quantity):
            raise unexpected_type_error("other", Quantity, other)
        return self.units.compatible(other.units)

    def __add__(self, other):
        if isinstance(other, Quantity):
            return make(self.quantity + other.get_as(self.units), self.units)
        return NotImplemented

    __iadd__ = __add__

    def __sub__(self, other):
        if isinstance(other, Quantity):
            return make(self.quantity - other.get_as(self.units), self.units)
        return NotImplemented

    __isub__ = __sub__

    def __neg__(self):
        return make(-self.quantity, self.units)

    def __bool__(self):
        return bool(self.quantity)

    def __eq__(self, other):
        if isinstance(other, Quantity):
            return self.units.compatible(other.units) and self.quantity == other.get_as(
                self.units
            )
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Quantity):
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

    def __abs__(self):
        return make(abs(self.quantity), self.units)

    def __lt__(self, other):
        if isinstance(other, Quantity):
            return self.quantity < other.get_as(self.units)
        return NotImplemented

    def __mul__(self, rhs):
        if isinstance(rhs, Quantity):
            return make(self.quantity * rhs.quantity, self.units * rhs.units)
        return make(self.quantity * rhs, self.units)

    __imul__ = __mul__

    def __rmul__(self, lhs):
        return make(lhs * self.quantity, self.units)

    def __truediv__(self, rhs):
        if isinstance(rhs, Quantity):
            return make(self.quantity / rhs.quantity, self.units / rhs.units)
        return make(self.quantity / rhs, self.units)

    __itruediv__ = __truediv__

    def __rtruediv__(self, lhs):
        return Quantity(lhs / self.quantity, ~self.units)

    def __pow__(self, exponent):
        if isinstance(exponent, numbers.Real):
            return make(self.quantity ** exponent, self.units ** exponent)
        return NotImplemented

    def __invert__(self):
        return make(1 / self.quantity, ~self.units)
