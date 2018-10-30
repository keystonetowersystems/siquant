from .dimensions import SIDimensions, dim_div, dim_mul, dim_pow, dim_str
from .util import immutable, flyweight


@flyweight
@immutable
class SIUnit:
    """SIUnit is a scaling of SI base unit dimensions.

    :cvar factory:
    :vartype factory: ``Callable[[_T, SIUnit], _Q]``

    :param scale: The scaling factor of base SI dimensions.
    :type scale: ``numbers.Real``
    :param dimensions: The base SI dimensions.
    :type dimensions: ``tuple``
    """

    __slots__ = ("scale", "dimensions", "__weakref__")

    #:
    #: The factory function which unit instances use to create quantities.
    #:
    #:    .. note::
    #:
    #:        SIUnit.factory is mapped to :class:`~siquant.quantities.Quantity`
    #:        in __init__ by default. However, it is *not* required to be a type,
    #:        and can be overwritten in client configuration.
    #:
    #:        It's purpose is to provide a consistent way to wrap values, and allow
    #:        simple extensibility.
    #:
    #:        :func:`~siquant.quantities.make` is just a wrapper around this factory.
    #:
    #:        .. code-block:: python
    #:
    #:            def ext_factory(q, u):
    #:                if isinstance(q, Vector):
    #:                    return VectorQuantity(q, u)
    #:                return Quantity(q, u)
    #:
    #:            SIUnit.factory = staticmethod(ext_factory)
    #:
    factory = None

    @staticmethod
    def Unit(scale=1.0, kg=0, m=0, s=0, k=0, a=0, mol=0, cd=0):
        """Create a new SIUnit with a scale of provided base units.

        :param scale: The linear scaling factor of base units.
        :type scale: ``numbers.Real``
        :param kg: The exponent of kilograms.
        :type kg: ``numbers.Real``
        :param m: The exponent of meters.
        :type m: ``numbers.Real``
        :param s: The exponent of seconds.
        :type s: ``numbers.Real``
        :param k: The exponent of degrees Kelvin.
        :type k: ``numbers.Real``
        :param a: The exponent of Amperes.
        :type a: ``numbers.Real``
        :param mol: The exponent of mols.
        :type mol: ``numbers.Real``
        :param cd: The exponent of candelas.
        :type cd: ``numbers.Real``
        :rtype: :class:`SIUnit`
        """
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
        """Get an SIUnit of equivalent dimensions with a scaling factor of 1.0.

        :rtype: :class:`~siquant.units.SIUnit`
        """
        return SIUnit(1.0, self.dimensions)

    def compatible(self, units):
        """Check whether the provided units are of the same dimensions.

        :param units: The units to check.
        :type units: :class:`~siquant.units.SIUnit`
        :rtype: ``bool``
        """
        return self.dimensions == units.dimensions

    def __call__(self, *args):
        """Create quantities these units for all arguments.

        :param args: The values to tag with units.
        :rtype: ``_Q`` = :class:`~siquant.quantities.Quantity`
        """
        return (self.factory(value, self) for value in args)

    def __mul__(self, rhs):
        if isinstance(rhs, SIUnit):
            return SIUnit(
                self.scale * rhs.scale, dim_mul(self.dimensions, rhs.dimensions)
            )
        return self.factory(rhs, self)

    def __rmul__(self, lhs):
        return self.factory(lhs, self)

    def __truediv__(self, rhs):
        if isinstance(rhs, SIUnit):
            return SIUnit(
                self.scale / rhs.scale, dim_div(self.dimensions, rhs.dimensions)
            )
        return self.factory(1 / rhs, self)

    def __rtruediv__(self, lhs):
        return self.factory(lhs, ~self)

    def __pow__(self, rhs):
        try:
            return SIUnit(self.scale ** rhs, dim_pow(self.dimensions, rhs))
        except TypeError:
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
