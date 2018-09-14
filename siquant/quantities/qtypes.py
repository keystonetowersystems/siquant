"""

"""

from .meta import Quantity, LinearQuantity

import siquant.units as u

class Scalar(metaclass=LinearQuantity, base_units=u.unity):
    pass

class Distance(metaclass=LinearQuantity, base_units=u.meters):

    def squared(self):
        return Area(self.get() ** 2)

    def cubed(self):
        return Volume(self.get() ** 3)

class Area(metaclass=LinearQuantity, base_units=u.square_meters):
    pass

class Volume(metaclass=LinearQuantity, base_units=u.cubic_meters):
    pass

class Time(metaclass=LinearQuantity, base_units=u.seconds):
    pass

class Velocity(metaclass=LinearQuantity, base_units=u.meters / u.seconds):
    pass

class Acceleration(metaclass=LinearQuantity, base_units=u.meters / u.seconds ** 2):
    pass

Acceleration.G = Acceleration(9.80665)

class Mass(metaclass=LinearQuantity, base_units=u.kilograms):
    pass

class Work(metaclass=LinearQuantity, base_units=u.joules):
    pass

class Power(metaclass=LinearQuantity, base_units=u.watts):
    pass

class Density(metaclass=LinearQuantity, base_units=u.kilograms / u.cubic_meters):
    pass

class Force(metaclass=LinearQuantity, base_units=u.newtons):
    pass

class Moment(metaclass=LinearQuantity, base_units=u.newton_meters):
    pass

class Stress(metaclass=LinearQuantity, base_units=u.pascals):
    pass

class MomentOfArea(metaclass=LinearQuantity, base_units=u.quartic_meters):
    pass

class SectionModulus(metaclass=LinearQuantity, base_units=u.cubic_meters):
    pass

class Angle(metaclass=LinearQuantity, base_units=u.radians):
    pass

class Frequency(metaclass=Quantity, base_units=u.hertz):
    pass

#todo: TrigAngle with cached trig functions?