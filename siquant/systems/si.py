from siquant.units import Unit

nano  = Unit.Unit(1 / 1e9)
micro = Unit.Unit(1 / 1e6)
milli = Unit.Unit(1 / 1000)
centi = Unit.Unit(1 / 100)
deci  = Unit.Unit(1 / 10)
unity = Unit.Unit(1)
deca  = Unit.Unit(10)
hecta = Unit.Unit(100)
kilo  = Unit.Unit(1000)
mega  = Unit.Unit(1e6)
giga  = Unit.Unit(1e9)
tera  = Unit.Unit(1e12)

meters = Unit.Unit(m=1)
kilograms = Unit.Unit(kg=1)
seconds = Unit.Unit(s=1)
kelvin = Unit.Unit(k=1)
amperes = Unit.Unit(a=1)
mols = Unit.Unit(mol=1)
candelas = Unit.Unit(cd=1)
radians = Unit.Unit(1)
steradians = Unit.Unit(1)

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

liters = Unit.Unit(1000) * centimeters ** 3
milliliters = milli * liters
microliters = micro * liters

grams = kilograms / kilo
milligrams = milli * grams
micrograms = micro * grams
tonnes = Unit.Unit(1000) * kilograms
kilotonnes = kilo * tonnes

nanoseconds  = nano * seconds
microseconds = micro * seconds
milliseconds = milli * seconds
minutes = Unit.Unit(60) * seconds
hours = Unit.Unit(60) * minutes
days = Unit.Unit(24) * hours
weeks = Unit.Unit(7) * days
years = Unit.Unit(365) * days

gals = centimeters / seconds ** 2
g_0 = Unit.Unit(9.80665) * meters / seconds ** 2

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
