from siquant.units import SIUnit

from .si import pascals

#:
inches = SIUnit.Unit(25.4 / 1000, m=1)

#:
thousandths = inches / SIUnit.Unit(1000)

#:
feet = SIUnit.Unit(12) * inches

#:
yards = SIUnit.Unit(3) * feet

#:
chains = SIUnit.Unit(22) * yards

#:
furlongs = SIUnit.Unit(10) * chains

#:
miles = SIUnit.Unit(8) * furlongs

#:
acres = SIUnit.Unit(1 / 640) * miles ** 2

#:
roods = SIUnit.Unit(1 / 4) * acres

#:
perches = SIUnit.Unit(1 / 40) * roods

#:
fluid_ounces = SIUnit.Unit(1.7339) * inches ** 3

#:
gills = SIUnit.Unit(5) * fluid_ounces

#:
pints = SIUnit.Unit(20) * fluid_ounces

#:
quarts = SIUnit.Unit(40) * fluid_ounces

#:
gallons = SIUnit.Unit(160) * fluid_ounces

#:
pounds = SIUnit.Unit(0.45359237, kg=1)

#:
ounces = pounds / SIUnit.Unit(16)

#:
stones = SIUnit.Unit(14) * pounds

#:
tons = SIUnit.Unit(2240) * pounds

#:
psi = SIUnit.Unit(6894.75729) * pascals

#:
ksi = SIUnit.Unit(1000) * psi

# todo: other imperial units
