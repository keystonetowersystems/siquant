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

    >>> from siquant.systems import si
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

Validation
==========

.. code-block:: pycon

    >>> from siquant.dimensions import force, area, stress
    >>> from siquant.systems import si

    >>> def normal_stress(force_q, area_q):
    ...     assert force_q.is_of(force)
    ...     assert area_q.is_of(area)
    ...     return force_q / area_q

    >>> stress_q = normal_stress(1 * si.newtons, 1 * si.meters ** 2)
    >>> stress_q.is_of(stress)
    True
    >>> stress_q.is_of(area)
    False

Sometimes you might want to check for dimensions that aren't provided by default.

.. code-block:: pycon

    >>> from siquant.dimensions import SIDimensions
    >>> from siquant.systems import si

    >>> new_dim = SIDimensions(kg=1, m=1, s=1, k=1, a=1, mol=1, cd=1)
    >>> dist_q = 1 * si.meters
    >>> dist_q.is_of(new_dim)
    False

Normalization
=============

.. code-block:: pycon

    >>> from siquant import ScalarQuantity
    >>> from siquant.systems import si

    >>> meters_cvt = ScalarQuantity.As(si.meters)

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

    >>> from siquant.units import SIUnit
    >>> fathom = SIUnit.Unit(1.8288, m=1)
    SIUnit(1.8288, (0, 1, 0, 0, 0, 0, 0))

Alternatively they can be derived:

.. code-block:: pycon

    >>> from siquant.systems import si
    >>> rpm = si.unity / si.minutes
    >>> rpm
    SIUnit(0.016667, (0, 0, -1, 0, 0, 0, 0))