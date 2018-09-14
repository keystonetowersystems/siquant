from functools import total_ordering

from .dispatch import bin_op_dispatcher

def equals(q1, q2):
    return type(q1) == type(q2) and q1._quantity == q2._quantity

def less_than(q1, q2):
    return type(q1) == type(q2) and q1._quantity < q2._quantity

class Quantity(type):

    def __new__(meta, name, bases, attrs, base_units=None):
        if base_units is None:
            raise ValueError('base_units is required to define a new quantity type')

        defined_slots = attrs.get('__slots__', ())

        def __init__(self, quantity, units=base_units):
            assert(base_units.matches_dimensions(units))
            self._quantity = units.normalize(quantity)

        def get_as(self, units):
            assert(base_units.matches_dimensions(units))
            return units.from_base_units(self._quantity)

        attrs = {
            **attrs,

            'base_units' : base_units,

            '__slots__' : ( '_quantity', *defined_slots),

            '__init__' : __init__,

            'get' : lambda self: self._quantity,

            'get_as' : get_as,

            '__eq__' : equals,

            '__lt__' : less_than,

            '__neg__' : lambda self: self.__class__(-self._quantity),

            '__str__' : lambda self: '%f %s' % (self._quantity, base_units.dimensions()),

            '__repr__' : lambda self: '%s(%f, units=%r)' % (self.__class__.__name__, self._quantity, base_units),

        }

        QType = super().__new__(meta, name, bases, attrs)

        return total_ordering(QType)

def add(q1, q2):
    assert(type(q1) == type(q2))
    return q1.__class__(q1._quantity + q2._quantity)

def sub(q1, q2):
    assert(type(q1) == type(q2))
    return q1.__class__(q1._quantity - q2._quantity)

class LinearQuantity(Quantity):

    def __new__(meta, name, bases, attrs, base_units=None):
        QType = super().__new__(meta, name, bases, attrs, base_units=base_units)

        (QType.__add__, QType.adder) = bin_op_dispatcher()
        (QType.__sub__, QType.subtracter) = bin_op_dispatcher()
        (QType.__mul__, QType.multiplier) = bin_op_dispatcher()
        (QType.__truediv__, QType.divider) = bin_op_dispatcher()

        QType.__rmul__ = QType.__mul__

        QType.multiplier(float, int)(lambda self, scalar: QType(self.get() * scalar))
        QType.divider(float, int)(lambda self, scalar: QType(self.get() / scalar))
        QType.divider(QType)(lambda self, other: self.get() / other.get())
        QType.adder(QType)(add)
        QType.subtracter(QType)(sub)

        def q_multiplier(op_type, result_type):
            def mul(q1, q2):
                return result_type(q1._quantity * q2._quantity, q1.base_units * q2.base_units)
            return QType.multiplier(op_type)(mul)
        QType.q_multiplier = q_multiplier

        def q_divider(op_type, result_type):
            def div(q1, q2):
                return result_type(q1._quantity / q2._quantity, q1.base_units / q2.base_units)
            return QType.divider(op_type)(div)
        QType.q_divider = q_divider

        return QType

