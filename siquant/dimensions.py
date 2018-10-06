abbreviations = ("kg", "m", "s", "k", "a", "mol", "cd")


def SIDimensions(kg=0, m=0, s=0, k=0, a=0, mol=0, cd=0):
    return (kg, m, s, k, a, mol, cd)


def dim_mul(dims1, dims2):
    return (
        dims1[0] + dims2[0],
        dims1[1] + dims2[1],
        dims1[2] + dims2[2],
        dims1[3] + dims2[3],
        dims1[4] + dims2[4],
        dims1[5] + dims2[5],
        dims1[6] + dims2[6],
    )


def dim_div(dims1, dims2):
    return (
        dims1[0] - dims2[0],
        dims1[1] - dims2[1],
        dims1[2] - dims2[2],
        dims1[3] - dims2[3],
        dims1[4] - dims2[4],
        dims1[5] - dims2[5],
        dims1[6] - dims2[6],
    )


def dim_pow(dims, exp):
    return (
        dims[0] * exp,
        dims[1] * exp,
        dims[2] * exp,
        dims[3] * exp,
        dims[4] * exp,
        dims[5] * exp,
        dims[6] * exp,
    )


def dim_str(dims):
    return "*".join(
        "%s**%g" % (unit_abbreviation, power)
        for unit_abbreviation, power in zip(abbreviations, dims)
        if power != 0
    )


angle = solid_angle = strain = ratio = SIDimensions()
mass = SIDimensions(kg=1)
distance = SIDimensions(m=1)
time = SIDimensions(s=1)
temperature = SIDimensions(k=1)
current = SIDimensions(a=1)
amount = SIDimensions(mol=1)
luminosity = SIDimensions(cd=1)
frequency = SIDimensions(s=-1)

speed = dim_div(distance, time)
acceleration = dim_div(speed, time)
jerk = dim_div(acceleration, time)
jounce = dim_div(jerk, time)

area = dim_pow(distance, 2)
volume = dim_pow(distance, 3)

density = dim_div(mass, volume)
volumetric_flow = dim_div(volume, time)

force = dim_mul(mass, acceleration)
impulse = momentum = dim_mul(force, time)
pressure = stress = dim_div(force, area)
hydrostatic_pressure = dim_mul(density, dim_mul(acceleration, distance))
surface_tension = stiffness = dim_div(force, distance)

energy = work = heat = dim_mul(force, distance)
power = dim_div(energy, time)

charge = dim_mul(current, time)
potential = dim_div(energy, current)
capacitance = dim_div(charge, potential)
resistance = impedance = reactance = dim_div(potential, current)
conductance = dim_div(current, potential)
magnetic_flux = dim_div(energy, current)
magnetic_flux_density = dim_div(magnetic_flux, area)
inductance = dim_mul(impedance, time)
luminous_flux = dim_mul(luminosity, solid_angle)
illuminance = dim_div(luminous_flux, area)

molarity = dim_div(amount, volume)
molality = dim_div(amount, mass)
molar_mass = dim_div(mass, amount)

entropy = heat_capacity = dim_div(energy, temperature)
specific_entropy = specific_heat_capacity = dim_div(entropy, mass)
temperature_gradient = dim_div(temperature, distance)
