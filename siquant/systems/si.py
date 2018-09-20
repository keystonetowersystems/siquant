from siquant.units import SIUnit
from siquant.quantities import Quantity

nano  = SIUnit.Unit(1 / 1e9)
micro = SIUnit.Unit(1 / 1e6)
milli = SIUnit.Unit(1 / 1000)
centi = SIUnit.Unit(1 / 100)
deci  = SIUnit.Unit(1 / 10)
unity = SIUnit.Unit(1)
deca  = SIUnit.Unit(10)
hecta = SIUnit.Unit(100)
kilo  = SIUnit.Unit(1000)
mega  = SIUnit.Unit(1e6)
giga  = SIUnit.Unit(1e9)
tera  = SIUnit.Unit(1e12)

meters = SIUnit.Unit(m=1)
kilograms = SIUnit.Unit(kg=1)
seconds = SIUnit.Unit(s=1)
kelvin = SIUnit.Unit(k=1)
amperes = SIUnit.Unit(a=1)
mols = SIUnit.Unit(mol=1)
candelas = SIUnit.Unit(cd=1)
radians = SIUnit.Unit(1)
steradians = SIUnit.Unit(1)

newtons = kilograms * meters / seconds ** 2
joules = newtons * meters
watts = joules / seconds
coulombs = amperes * seconds
volts = watts / amperes
farads = coulombs / volts
ohms = volts / amperes
siemens = ~ohms
webers = volts * seconds
teslas = webers / meters ** 2
henrys = webers / amperes
lumens = candelas * steradians
lux = lumens / meters ** 2
becquerels = ~seconds

nanometers  = nano * meters
micrometers = micro * meters
millimeters = milli * meters
centimeters = centi * meters
decimeters  = deci * meters
decameters  = deca * meters
hectameters = hecta * meters
kilometers  = kilo * meters

liters = SIUnit.Unit(1000) * centimeters ** 3
milliliters = milli * liters
microliters = micro * liters

grams = kilograms / kilo
milligrams = milli * grams
micrograms = micro * grams
tonnes = SIUnit.Unit(1000) * kilograms
kilotonnes = kilo * tonnes

nanoseconds  = nano * seconds
microseconds = micro * seconds
milliseconds = milli * seconds
minutes = SIUnit.Unit(60) * seconds
hours = SIUnit.Unit(60) * minutes
days = SIUnit.Unit(24) * hours
weeks = SIUnit.Unit(7) * days
years = SIUnit.Unit(365) * days

gals = centimeters / seconds ** 2
g_0 = SIUnit.Unit(9.80665) * meters / seconds ** 2

millijoules = milli * joules
kilojoules = kilo * joules
megajoules = mega * joules
gigajoules = giga * joules

milliwatts = milli * watts
kilowatts = kilo * watts
megawatts = mega * watts
gigawatts = giga * watts

millinewtons = milli * newtons
kilonewtons = kilo * newtons

# etc ...
