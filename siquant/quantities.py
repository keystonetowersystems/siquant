try:
    from operator import matmul
except ImportError:
    pass  # matmul not supported

from functools import total_ordering

from .exceptions import UnitMismatchError, unexpected_type_error
from .util import immutable


def make(quantity, units):
    """Entry point for creating quantities consistently

    :param quantity: The value to tag with specific units.
    :type quantity: ``_T``
    :param units: The units of this quantity.
    :type units: :class:`~siquant.units.SIUnit`
    :rtype: ``_Q`` = :class:`~Quantity`
    """
    return units.factory(quantity, units)


def converter(units):
    """Create a converter function which will return Quantities.

    :param units: The units to convert a quantity to.
    :type units: :class:`~siquant.units.SIUnit`
    :rtype: ``Callable[[Any], _Q]``
    """

    def _converter(value):
        if isinstance(value, Quantity):
            return value.cvt_to(units)
        return make(value, units)

    return _converter


def is_of(dimensions):
    """Create a validator function which checks if a value matches expected dimensions.

    .. seealso::

        Predefined :mod:`~siquant.dimensions`.

        Creating new :func:`~siquant.dimensions.SIDimensions`.

    :param dimensions: The expected dimensions.
    :type dimensions: ``tuple``
    :rtype: ``Callable[[Any], bool]``
    """

    if not isinstance(dimensions, tuple):
        raise unexpected_type_error("dimensions", tuple, dimensions)
    if not len(dimensions) == 7:
        raise ValueError("Dimensions tuple must have 7 elements.", dimensions)

    def _validator(value):
        if not isinstance(value, Quantity):
            return False
        return value.is_of(dimensions)

    return _validator


@immutable
@total_ordering
class Quantity:
    """Quantity wraps a value with units and provides arithmetic passthrough operations.

    .. note::

        Creation of Quantity directly is discouraged.

        The preferred method are:

        q = value * si.meters

        q = make(value, si.meters)

        Both of these methods delegate instantiation to
        :attr:`~siquant.units.SIUnit.factory` in order to
        more easily support clean extensibility.

    :ivar quantity: The wrapped value. read only.
    :vartype quantity: ``_T``
    :ivar units: The units of this quantity. read only.
    :vartype units: :class:`~siquant.units.SIUnit`

    :param quantity: The quantity to be wrapped.
    :type quantity: ``_T``
    :param units: The units the quantity's value is expressed in.
    :type units: :class:`~siquant.units.SIUnit`
    """

    __slots__ = ("quantity", "units")

    def __init__(self, quantity, units):
        if isinstance(quantity, Quantity):
            units = quantity.units * units
            quantity = quantity.quantity
        super().__setattr__("quantity", quantity)
        super().__setattr__("units", units)

    def is_of(self, dimensions):
        """

        :param dimensions:
        :return: ``bool``
        """
        return self.units.dimensions == dimensions

    def get_as(self, units):
        """

        :param units: The units to express the underlying value in.
        :type units: :class:`~siquant.units.SIUnit`
        :rtype: ``_T``
        """
        if self.units == units:
            return self.quantity
        if not self.units.compatible(units):
            raise UnitMismatchError(self.units, units)
        return self.units.scale / units.scale * self.quantity

    def cvt_to(quantity, units):
        """Create an equivalent Quantity expressed in the provided units.

        :param units: The units to express this quantity in.
        :type units: :class:`~siquant.units.SIUnit`
        :return: ``_Q`` = :class:`~siquant.quantities.Quantity`
        """
        return make(quantity.get_as(units), units)

    def compatible(self, other):
        """

        :param other: The quantity to check for dimensional compatibility.
        :type other: ``_Q`` = :class:`~siquant.quantities.Quantity`
        :rtype: bool
        """
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

    def __matmul__(self, rhs):
        if isinstance(rhs, Quantity):
            return make(matmul(self.quantity, rhs.quantity), self.units * rhs.units)
        return make(matmul(self.quantity, rhs), self.units)

    __imatmul__ = __matmul__

    def __rmatmul__(self, lhs):
        return make(matmul(lhs, self.quantity), self.units)

    def __truediv__(self, rhs):
        if isinstance(rhs, Quantity):
            return make(self.quantity / rhs.quantity, self.units / rhs.units)
        return make(self.quantity / rhs, self.units)

    __itruediv__ = __truediv__

    def __rtruediv__(self, lhs):
        return Quantity(lhs / self.quantity, ~self.units)

    def __pow__(self, exponent):
        try:
            return make(self.quantity ** exponent, self.units ** exponent)
        except TypeError:
            return NotImplemented

    def __invert__(self):
        return make(1 / self.quantity, ~self.units)
