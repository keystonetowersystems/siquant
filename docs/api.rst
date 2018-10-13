.. _api:

=============
API Reference
=============


Quantity
========

.. autofunction:: siquant.quantities.make

.. autofunction:: siquant.quantities.are_of

.. autofunction:: siquant.quantities.validator

.. autofunction:: siquant.quantities.converter

.. autoclass:: siquant.quantities.Quantity
    :members:


Units
=====

.. autoclass:: siquant.units.SIUnit
    :members:
    :exclude-members: factory

    .. autoattribute:: factory
        :annotation:


Dimensions
==========

.. currentmodule:: siquant.dimensions

.. autofunction:: SIDimensions

.. autofunction:: dim_mul

.. autofunction:: dim_div

.. autofunction:: dim_pow

.. autofunction:: dim_str

Helpers
=======

A number of units and dimensions are predefined to make getting started quick and easy.

Provided SI Units
-----------------

.. automodule:: siquant.systems.si
    :members:
    :member-order: bysource

Provided Imperial Units
-----------------------

.. automodule:: siquant.systems.imperial
    :members:
    :member-order: bysource

Provided Dimensions
-------------------

.. automodule:: siquant.dimensions
    :members:
    :exclude-members: SIDimensions, dim_mul, dim_div, dim_pow, dim_str
    :member-order: bysource