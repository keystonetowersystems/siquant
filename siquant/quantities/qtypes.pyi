from typing import Union, Callable, Any
import numpy as np
import siquant.units as u

numeric_t = Union[float, np.ndarray]

binary_op_t = Callable[[Any, Any], Any]

registration_t = Callable[[*Any], binary_op_t]

class Quantity:

    def get(self) -> numeric_t: ...

    def get_as(self, units: u.Unit) -> numeric_t: ...

    @staticmethod
    def multiplier(op_type) -> registration_t: ...

    @staticmethod
    def divider(op_type) -> registration_t: ...

    @staticmethod
    def adder(op_type) -> registration_t: ...

    @staticmethod
    def subtracter(op_type) -> registration_t: ...

    @staticmethod
    def q_multiplier(op_type, result_type) -> binary_op_t: ...

    @staticmethod
    def q_divider(op_type, result_type) -> binary_op_t: ...

    def __add__(self, other) -> Any: ...

    def __sub__(self, other) -> Any: ...

    def __mul__(self, other) -> Any: ...

    def __truediv__(self, other) -> Any: ...

class Distance(Quantity):

    def __init__(self, quantity: numeric_t, units: u.Unit = u.meters): ...

    def squared(self) -> Area: ...

    def cubed(self) -> Volume: ...

class Area(Quantity):

    def __init__(self, quantity: numeric_t, units: u.Unit = u.square_meters): ...

class Volume(Quantity):

    def __init__(self, quantity: numeric_t, units: u.Unit = u.cubic_meters): ...

class Time(Quantity):

    def __init__(self, quantity: numeric_t, units: u.Unit = u.seconds): ...

class Velocity(Quantity):

    def __init__(self, quantity: numeric_t, units: u.Unit = u.meters / u.seconds): ...

class Acceleration(Quantity):

    def __init__(self, quantity: numeric_t, units: u.Unit = u.meters / u.seconds ** 2): ...

class Mass(Quantity):

    def __init__(self, quantity: numeric_t, units: u.Unit = u.kilograms): ...

class Density(Quantity):

    def __init__(self, quantity: numeric_t, units: u.Unit = u.kilograms / u.meters ** 3): ...

class Force(Quantity):

    def __init__(self, quantity: numeric_t, units: u.Unit = u.newtons): ...

class Moment(Quantity):

    def __init__(self, quantity: numeric_t, units: u.Unit = u.newton_meters): ...

class Stress(Quantity):

    def __init__(self, quantity: numeric_t, units: u.Unit = u.pascals): ...

class MomentOfArea(Quantity):

    def __init__(self, quantity: numeric_t, units: u.Unit = u.quartic_meters): ...

class SectionModulus(Quantity):

    def __init__(self, quantity: numeric_t, units: u.Unit = u.cubic_meters): ...

class Angle(Quantity):

    def __init__(self, quantity: numeric_t, units: u.Unit = u.radians): ...