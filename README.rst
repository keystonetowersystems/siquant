========================================
``siquant``: Simple Dimensional Analysis
========================================

.. image:: https://badge.fury.io/py/siquant.svg
   :target: https://badge.fury.io/py/siquant
   :alt: PyPi Package

.. image:: https://travis-ci.com/keystonetowersystems/siquant.svg?branch=master
   :target: https://travis-ci.com/keystonetowersystems/siquant
   :alt: Build Status

.. image:: https://coveralls.io/repos/github/keystonetowersystems/siquant/badge.svg?branch=master
   :target: https://coveralls.io/github/keystonetowersystems/siquant?branch=master
   :alt: Code Coverage

``siquant`` is a simple pure python 3 library to make dimensional analysis painless.

---------------
Getting Started
---------------

Dimensional Analysis
====================

.. code-block:: pycon

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
    >>> torque.get_as(si.newtons)
    Traceback (most recent call last):
      ...
    siquant.exceptions.UnitMismatchError: ...

    >>> torque = torque.cvt_to(si.newtons * si.meters)
    >>> torque.quantity
    5000000.0
    >>> str(torque.units)
    '1*kg**1*m**2*s**-2'

Some limited imperial units are also provided:

.. code-block:: pycon

    >>> from siquant import imperial, si
    >>> floor_space = 200 * si.meters ** 2
    >>> dollars_per_sq_ft = 250 / imperial.feet ** 2
    >>> price = floor_space * dollars_per_sq_ft
    >>> round(price.get_as(si.unity), 2)
    538195.52

Validation
==========

.. code-block:: pycon

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

Alternatively, the desired dimensionality can be captured in a validator:

.. code-block:: pycon

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

.. code-block:: pycon

    >>> from siquant import si
    >>> from siquant.dimensions import SIDimensions

    >>> new_dim = SIDimensions(kg=1, m=1, s=1, k=1, a=1, mol=1, cd=1)
    >>> dist = 1 * si.meters
    >>> dist.is_of(new_dim)
    False

For performance reasons, dimensionality is stored as a naked tuple. New dimensionalities
can be derived much the same as with units, though the transformation functions must be
invoke explicitly.

.. code-block:: pycon

    >>> from siquant.dimensions import dim_div, jounce_t, time_t
    >>> crackle_t = dim_div(jounce_t, time_t)
    >>> pop_t = dim_div(crackle_t, time_t)

Normalization
=============

.. code-block:: pycon

    >>> from siquant import si, converter

    >>> meters_cvt = converter(si.meters)

    >>> dist_q = meters_cvt(1000 * si.millimeters)
    >>> dist_q.quantity
    1

    >>> dist_q = meters_cvt(1000 * si.meters)
    >>> dist_q.quantity
    1000

    >>> dist_q = meters_cvt(1000)
    >>> dist_q.quantity
    1000

---------
New Units
---------

SIUnit can be created directly by factory:

.. code-block:: pycon

    >>> from siquant import SIUnit
    >>> fathom = SIUnit.Unit(1.8288, m=1)
    SIUnit(1.8288, (0, 1, 0, 0, 0, 0, 0))

Alternatively they can be derived:

.. code-block:: pycon

    >>> from siquant import si
    >>> rpm = si.unity / si.minutes
    >>> rpm
    SIUnit(0.016667, (0, 0, -1, 0, 0, 0, 0))

-----------------------------
Extending Quantity Operations
-----------------------------

.. code-block:: pycon

    >>> from siquant import SIUnit, Quantity, make, si
    >>> class Vector:
            __mul__ = __rmul__ = lambda s, scalar: Vector(s.x * scalar, s.y * scalar)
            dot = lambda s, o: s.x * o.x + s.y * o.y

    >>> class ExtendedQuantity(Quantity):
            __slots__ = ()

            def dot_product(self, other):
                assert isinstance(self.quantity, Vector)
                assert isinstance(other.quantity, Vector)
                return make(self.quantity.dot(other.quantity), self.units * other.units)

    >>> SIUnit.factory = ExtendedQuantity

    >>> distance = 100 * si.meters
    >>> distance_vector = distance * Vector(1, 0)
    >>> distance_vector.get_as(si.meters)
    Vector(100, 0)
    >>> scalar_product = distance_vector.dot(distance_vector)
    >>> scalar_product.get_as(si.meters)
    10000