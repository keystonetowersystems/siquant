class Unit:

    def __init__(self, factor, m=0, kg=0, s=0, amp=0, cd=0, mol=0, k=0):
        """

        Args:
            factor:
            m:
            kg:
            s:
            amp:
            cd:
            mol:
            k:
        """
        self._factor = factor
        self._units = {
            'm'   : m,
            'kg'  : kg,
            's'   : s,
            'k'   : k,
            'amp' : amp,
            'cd'  : cd,
            'mol' : mol
        }

    def normalize(self, quantity):
        return quantity * self._factor

    def from_base_units(self, normalized_quantity):
        return normalized_quantity / self._factor

    def convert(self, reference_unit):
        assert(self.matches_dimensions(reference_unit))
        return reference_unit.from_base_units(self._factor)

    def _exponent(self, unit_key):
        """

        Args:
            unit_key:

        Returns:

        """
        return self._units[unit_key]

    def __mul__(self, other):
        """

        Args:
            other: Unit:

        Returns:

        """
        new_units = {
            key: value + other._units[key]
            for key, value in self._units.items()
        }
        return Unit(self._factor * other._factor, **new_units)

    __rmul__ = __mul__

    def __truediv__(self, other):
        """

        Args:
            other:

        Returns:

        """
        new_units = {
            key: value - other._units[key]
            for key, value in self._units.items()
        }
        return Unit(self._factor / other._factor, **new_units)

    def __pow__(self, exp):
        """

        Args:
            exp:

        Returns:

        """
        new_units = {
            key: value * exp
            for key, value in self._units.items()
        }
        return Unit(self._factor ** exp, **new_units)

    def dimensions(self):
        return '*'.join(
            '%s^%i' % (unit, exp)
            for (unit, exp)
            in self._units.items()
            if exp != 0
        )

    def __eq__(self, other):
        return self._factor == other._factor and self.matches_dimensions(other)

    def matches_dimensions(self, other):
        return all(self._units[key] == other._units[key] for key in self._units)

    def __str__(self):
        return '%f %s' % (self._factor, self.dimensions())

    def __repr__(self):
        return 'Unit(%f, m=%i, kg=%i, s=%i, k=%i, amp=%i, cd=%i, mol=%i)' % (
            self._factor,
            self._units['m'],
            self._units['kg'],
            self._units['s'],
            self._units['k'],
            self._units['amp'],
            self._units['cd'],
            self._units['mol']
        )

# SI Convenience (unitless)

nano = Unit(1 / 1e9)
micro = Unit(1 / 1e6)
milli = Unit(1 / 1e3)
centi = Unit(1 / 1e2)
deci = Unit(1 / 10)
unity = Unit(1)
deca = Unit(10)
hecta = Unit(1e2)
kilo = Unit(1e3)
mega = Unit(1e6)
giga = Unit(1e9)

# base units

meters = Unit(1, m=1)
kilograms = Unit(1, kg=1)
seconds = Unit(1, s=1)
candelas = Unit(1, cd=1)
mols = Unit(1, mol=1)
amps = Unit(1, amp=1)
kelvin = Unit(1, k=1)

# Distance

centimeters = centi * meters
millimeters = milli * meters
inches = Unit(25.4) * millimeters
feet = Unit(12) * inches
yards = Unit(3) * feet
miles = Unit(5280)

square_meters = meters ** 2
square_centimeters = centimeters ** 2
square_millimeters = millimeters ** 2
square_inches = inches ** 2
square_feet = feet ** 2

cubic_meters = meters ** 3
cubic_centimeters = centimeters ** 3
cubic_millimeters = millimeters ** 3

quartic_meters = meters ** 4
quartic_centimeters = centimeters ** 4
quartic_millimeters = millimeters ** 4

# Mass

grams = kilograms / kilo
tonnes = Unit(1000) * kilograms
pounds = Unit(0.45359237) * kilograms
slugs = Unit(14.5939) * kilograms

# Time

minutes = Unit(60) * seconds
hours = Unit(60) * minutes

# Velocity

meters_per_second = meters / seconds
miles_per_hour = miles / hours

# Force

newtons = kilograms * meters / seconds ** 2
kilonewtons = kilo * newtons
dynes = grams * centimeters / seconds ** 2
pound_force = slugs * feet / seconds ** 2

# Pressure / Stress

pascals = newtons / meters ** 2
kilopascals = kilo * pascals
megapascals = mega * pascals
gigapascals = giga * pascals

atmospheres = Unit(101325) * pascals
torrs = atmospheres / Unit(760)


joules = Unit(1, kg=1, m=2, s=-2)
watts = joules / seconds

volts = watts / amps

newton_meters = newtons * meters
kilonewton_meters = kilonewtons * meters
pound_feet = pound_force * feet

# Angles

PI = 3.14159265358979323846264338327950288419716939937510582097

radians = Unit(1)
degrees = radians * Unit(PI / 180)
arcminutes = degrees / Unit(60)
arcseconds = arcminutes / Unit(60)


hertz = Unit(1) / seconds
rpm = Unit(1) / minutes

