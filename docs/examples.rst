.. _examples:

``siquant`` by Example
======================

Keeping Track of Units
----------------------

.. -basics-

.. doctest::

    >>> from siquant import si

    >>> force = 100 * si.kilonewtons
    >>> moment_arm = 50 * si.meters
    >>> torque = force * moment_arm
    >>> torque.quantity
    5000

    >>> str(torque.units)
    '1000*kg**1*m**2*s**-2'

    >>> torque.get_as(si.newtons * si.meters)
    5000000.0

    >>> torque.get_as(si.newtons) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      ...
    siquant.exceptions.UnitMismatchError: ...

    >>> torque = torque.cvt_to(si.newtons * si.meters)
    >>> torque.quantity
    5000000.0

    >>> str(torque.units)
    '1*kg**1*m**2*s**-2'

Some limited imperial units are also provided:

.. doctest::

    >>> from siquant import imperial, si
    >>> floor_space = 200 * si.meters ** 2
    >>> dollars_per_sq_ft = 250 / imperial.feet ** 2
    >>> price = floor_space * dollars_per_sq_ft
    >>> round(price.get_as(si.unity), 2)
    538195.52

.. -end-basics-

Limitations
~~~~~~~~~~~

Unit transformations are purely defined by linear scaling at this time. It is conceivable
to create a drop in replacement that would properly handle non-linear transformations, but
it is not under consideration at this time.

As such, units of **temperature** other than degrees Kelvin are not provided by default. Client
code should therefore treat any other units of temperature as discrete differences or is
responsible for applying the corrective offsets.

Validation
----------

For validation purposes only the :mod:`~siquant.dimensions` of a quantity or unit are
considered.

The underlying value can be retrieved at whatever scale is desired by
calling :meth:`~siquant.quantities.Quantity.get_as`.

.. -validation-

.. doctest::

    >>> from siquant.dimensions import force_t, area_t, stress_t
    >>> from siquant import si

    >>> def normal_stress(force, area):
    ...     assert force.is_of(force_t)
    ...     assert area.is_of(area_t)
    ...     return force / area

    >>> stress = normal_stress(1 * si.newtons, 1 * si.meters ** 2)
    >>> stress.is_of(stress_t)
    True
    >>> stress.is_of(area_t)
    False
    >>> stress.get_as(si.kilopascals)
    0.001

Alternatively, the desired dimensionality can be captured in a validator:

.. doctest::

    >>> from siquant import si, is_of
    >>> from siquant.dimensions import distance_t

    >>> distance_validator = is_of(distance_t)
    >>> distance_validator(10 * si.meters)
    True
    >>> distance_validator(10 * si.millimeters)
    True
    >>> distance_validator(10)
    False
    >>> distance_validator(10 * si.newtons)
    False

Sometimes you might want to check for dimensions that aren't provided by default.

.. doctest::

    >>> from siquant import si
    >>> from siquant.dimensions import SIDimensions

    >>> new_dim = SIDimensions(kg=1, m=1, s=1, k=1, a=1, mol=1, cd=1)
    >>> dist = 1 * si.meters
    >>> dist.is_of(new_dim)
    False

For performance reasons, dimensionality is stored as a naked tuple. New dimensions
can be derived much the same as with units, though the transformation functions must be
invoked explicitly.

.. doctest::

    >>> from siquant.dimensions import dim_div, jounce_t, time_t
    >>> crackle_t = dim_div(jounce_t, time_t)
    >>> pop_t = dim_div(crackle_t, time_t)

Limitations
~~~~~~~~~~~

For simplicity and performance, there is no distinction between quantities of the same
dimensionality. This is true, even when checking via SIUnit instances. So care must
still be taken.

.. doctest::

    >>> from siquant.dimensions import angle_t, strain_t
    >>> from siquant import si

    >>> length = 10 * si.meters
    >>> deflection = 1 * si.millimeters
    >>> strain = deflection / length

    >>> strain.is_of(strain_t)
    True

    >>> strain.is_of(angle_t)
    True

    >>> strain.units.compatible(si.radians)
    True

.. -end-validation-

Normalization
-------------

If a quantity is often required at a specific scale, it may be desirable to normalize it.

It is normally preferred to extract values via :meth:`~siquant.quantities.Quantity.get_as`
however, it is faster to access quantity directly when the scale and dimensions have
already been verified.

.. doctest::

    >>> from siquant import si, converter

    >>> meters_cvt = converter(si.meters)

    >>> dist_q = meters_cvt(1000 * si.millimeters)
    >>> dist_q.quantity
    1.0

    >>> dist_q = meters_cvt(1000 * si.meters)
    >>> dist_q.quantity
    1000

    >>> dist_q = meters_cvt(1000)
    >>> dist_q.quantity
    1000

Custom Units
------------

A number of units are predefined in :mod:`~siquant.systems.si` and
:mod:`~siquant.systems.imperial`, but this list is by no means exhaustive, or perhaps
the problem is best considered in plank units.

New SIUnit`s can be created directly by factory:


.. doctest::

    >>> from siquant import SIUnit
    >>> fathom = SIUnit.Unit(1.8288, m=1)
    >>> fathom
    SIUnit(1.828800, (0, 1, 0, 0, 0, 0, 0))

Alternatively, they can be derived from existing units:

.. doctest::

    >>> from siquant import si
    >>> rpm = si.unity / si.minutes
    >>> rpm
    SIUnit(0.016667, (0, 0, -1, 0, 0, 0, 0))

Custom Quantities
-----------------

By default, Quantity provides the interface of the basic python arithmetic operatiors,
and delegates the transformation to the wrapped values, and returns a new wrapped
Quantity.

If other operations are desired, Quantity can be easily replaced or extended:

.. doctest::

    >>> from siquant import SIUnit, Quantity, make, si
    >>> class Vector:
    ...     def __init__(self, x, y):
    ...         self.x = x
    ...         self.y = y
    ...
    ...     def __rmul__(self, other):
    ...         return Vector(self.x * other, self.y * other)
    ...
    ...     def dot(self, other):
    ...         return self.x * other.x + self.y * other.y
    ...
    ...     def __repr__(self):
    ...         return 'Vector(%d, %d)' % (self.x, self.y)
    ...
    >>> class ExtendedQuantity(Quantity):
    ...     __slots__ = ()
    ...
    ...     def dot_product(self, other):
    ...         assert isinstance(self.quantity, Vector)
    ...         assert isinstance(other.quantity, Vector)
    ...         return make(
    ...             self.quantity.dot(other.quantity),
    ...             self.units * other.units
    ...         )
    ...
    >>> SIUnit.factory = ExtendedQuantity
    >>> distance = 100 * si.meters
    >>> distance
    ExtendedQuantity(100, SIUnit(1.000000, (0, 1, 0, 0, 0, 0, 0)))
    >>> distance_vector = distance * Vector(1, 0)
    >>> distance_vector.get_as(si.meters)
    Vector(100, 0)
    >>> scalar_product = distance_vector.dot_product(distance_vector)
    >>> scalar_product.get_as(si.meters ** 2)
    10000
