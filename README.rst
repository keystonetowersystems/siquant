=================================
``siquant``: Dimensional Analysis
=================================
.. image:: https://readthedocs.org/projects/siquant/badge/?version=latest
   :target: https://siquant.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

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

It is a small, flexible codebase aimed at 2 specific related problems: implicit unit
tracking, and ensuring semantic correctness (fail fast) with minimal overhead.

---------------
Getting Started
---------------

0. Install ``siquant``

``pip3 install siquant==4.0.0b9``

1. Implicit Unit Tracking:

.. code-block:: pycon

    >>> from siquant import si
    >>> a = 10 * si.millimeters
    >>> b = 10 * si.kilometers
    >>> ab = a * b
    >>> ab.quantity
    100
    >>> str(ab.units)
    '1*m**2'
    >>> ab.get_as(si.millimeters ** 2)
    100000000.0

2. Dimensional Analysis:

.. code-block:: pycon

    >>> from siquant.dimensions import area_t
    >>> from siquant import imperial, si

    >>> def real_estate_price(area):
    ...     assert area.is_of(area_t) #  or raise if at application/lib dmz
    ...     monies_per_square_foot = 100 / imperial.feet ** 2
    ...     return area * monies_per_square_foot
    ...
    >>> house_price = real_estate_price(100 * si.meters ** 2)
    >>> house_price
    Quantity(10000, SIUnit(10.763910, (0, 0, 0, 0, 0, 0, 0)))
    >>> round(house_price.get_as(si.unity))
    107639

----------------
Online Resources
----------------

``siquant`` is released under the `MIT LICENSE <https://github.com/keystonetowersystems/siquant/blob/master/LICENSE>`_.

Releases are hosted in the `pypi package repository <https://pypi.org/project/siquant/>`_.

More detailed documentation and examples can be found on `readthedocs <https://siquant.readthedocs.io/en/latest>`_.


