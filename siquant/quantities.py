try:
    from operator import matmul
except ImportError:
    pass  # matmul not supported

from copy import copy, deepcopy
from functools import total_ordering

from .exceptions import UnitMismatchError, unexpected_type_error
from .util import immutable
from .unitless import Unitless


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


def validator(dimensions):
    """Create a validator function which checks if a value matches expected dimensions.

    .. seealso::

        Predefined :mod:`~siquant.dimensions`.

        Creating new :func:`~siquant.dimensions.SIDimensions`.

    :param dimensions: The expected dimensions.
    :type dimensions: ``tuple``
    :rtype: ``Callable[[Any, ...], bool]``
    """

    if not isinstance(dimensions, tuple):
        raise unexpected_type_error("dimensions", tuple, dimensions)
    if not len(dimensions) == 7:
        raise ValueError("Dimensions tuple must have 7 elements.", dimensions)

    def _validator(*values):
        return are_of(dimensions, *values)

    return _validator


def are_of(dimensions, *quantities):
    """Check if quantities all match dimensions.

    :param dimensions: The expected dimensionality.
    :type dimensions: ``tuple``
    :param quantities: Variadic. The instances to check against.
    :rtype: ``bool``
    """
    try:
        return all(q.is_of(dimensions) for q in quantities)
    except AttributeError:
        return False


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

    def round_to(self, units, places=0):
        """Create an equivalent Quantity rounded in provided units.

        :param units: The units to express the quantity in.
        :type units: :class:`~siquant.units.SIUnit`
        :param places: The number of decimal places to round to.
        :type places: ``int``
        :rtype: ``_Q`` = :class:`~siquant.quantities.Quantity`
        """
        return make(round(self.get_as(units), places), units)

    def compatible(self, other):
        """

        :param other: The quantity to check for dimensional compatibility.
        :type other: ``_Q`` = :class:`~siquant.quantities.Quantity`
        :rtype: bool
        """
        if isinstance(other, Unitless):
            other = make(other, self.units.Unit())
        if not isinstance(other, Quantity):
            raise unexpected_type_error("other", Quantity, other)
        return self.units.compatible(other.units)

    def __abs_epsilon(self, atol=1e-6):
        if isinstance(atol, Quantity):
            return atol
        return atol * self.units

    def __rel_epsilon(self, other, rtol=1e-9):
        return rtol * max(abs(self), abs(other), 1 * self.units)

    def abs_approx(self, other, atol=1e-6):
        return self.approx(other, rtol=0, atol=atol)

    def rel_approx(self, other, rtol=1e-9):
        return self.approx(other, rtol=rtol, atol=0)

    def approx(self, other, rtol=1e-9, atol=1e-6):
        """

        :raises: ``TypeError`` if other is not a Quantity

        :param other:
        :param rtol:
        :type rtol:
        :param atol:
        :type atol:
        :return:
        """
        if not self.compatible(other):
            return False

        epsilon = max(self.__rel_epsilon(other, rtol), self.__abs_epsilon(atol))
        return abs(other - self) <= epsilon

    def __add__(self, other):
        if isinstance(other, Quantity):
            return make(self.quantity + other.get_as(self.units), self.units)
        if isinstance(other, Unitless):
            return self + make(other, self.units.Unit())
        return NotImplemented

    def __radd__(self, other):
        if isinstance(other, Unitless):
            return make(other, self.units.Unit()) + self
        return NotImplemented

    __iadd__ = __add__

    def __sub__(self, other):
        if isinstance(other, Quantity):
            return make(self.quantity - other.get_as(self.units), self.units)
        if isinstance(other, Unitless):
            return self - make(other, self.units.Unit())
        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, Unitless):
            return make(other, self.units.Unit()) - self
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
        if isinstance(other, Unitless):
            return self == make(other, self.units.Unit())
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Quantity):
            return not self.units.compatible(
                other.units
            ) or self.quantity != other.get_as(self.units)
        if isinstance(other, Unitless):
            return self != make(other, self.units.Unit())
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

    def __float__(self):
        return float(self.quantity)

    def __int__(self):
        return int(self.quantity)

    def __len__(self):
        return len(self.quantity)

    def __iter__(self):
        return (make(q, self.units) for q in self.quantity)

    def __getitem__(self, idx):
        return make(self.quantity[idx], self.units)

    def __copy__(self):
        return make(copy(self.quantity), self.units)

    def __deepcopy__(self, memodict):
        return make(deepcopy(self.quantity), self.units)
