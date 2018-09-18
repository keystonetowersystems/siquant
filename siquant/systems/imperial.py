from siquant.units import Unit

inches = Unit.Unit(25.4 / 1000, m=1)
thousandths = inches / Unit.Unit(1000)
feet = Unit.Unit(12) * inches
yards = Unit.Unit(3) * feet
chains = Unit.Unit(22) * yards
furlongs = Unit.Unit(10) * chains
miles = Unit.Unit(8) * furlongs

acres = Unit.Unit(1 / 640) * miles ** 2
roods = Unit.Unit(1 / 4) * acres
perches = Unit.Unit(1 / 40) * roods

fluid_ounces = Unit.Unit(1.7339) * inches ** 3
gills = Unit.Unit(5) * fluid_ounces
pints = Unit.Unit(20) * fluid_ounces
quarts = Unit.Unit(40) * fluid_ounces
gallons = Unit.Unit(160) * fluid_ounces

pounds = Unit.Unit(0.45359237, kg=1)
ounces = pounds / Unit.Unit(16)
stones = Unit.Unit(14) * pounds
tons = Unit.Unit(2240) * pounds

#todo: ...