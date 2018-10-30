abbreviations = ("kg", "m", "s", "k", "a", "mol", "cd")


def SIDimensions(kg=0, m=0, s=0, k=0, a=0, mol=0, cd=0):
    """Create a dimensionality tuple with base si units of provided exponents.

    :param kg: The exponent of Kilograms.
    :type kg: ``numbers.Real``
    :param m: The exponent of Meters.
    :type m: ``numbers.Real``
    :param s: The exponent of Seconds.
    :type s: ``numbers.Real``
    :param k: The exponent of Kelvin.
    :type k: ``numbers.Real``
    :param a: The exponent of Amperes.
    :type a: ``numbers.Real``
    :param mol: The exponent of Mols.
    :type mol: ``numbers.Real``
    :param cd: The exponent of Candelas.
    :type cd: ``numbers.Real``
    :rtype: ``tuple``
    """
    return (kg, m, s, k, a, mol, cd)


def dim_mul(dims1, dims2):
    """Create a new dimensionality for the multiplication of dims1 by dims2.

    :param dims1: Numerator dimensions.
    :type dims1: ``tuple``
    :param dims2: Other numerator dimensions.
    :type dims2: ``tuple``
    :rtype: ``tuple``
    """
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
    """Create a new dimensionality tuple for the division of dims1 by dims2.

    :param dims1: The numerator dimensions.
    :type dims1: ``tuple``
    :param dims2: The divisor dimensions.
    :type dims2: ``tuple``
    :rtype: ``tuple``
    """
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
    """Create a new dimensionality tuple for the exponentiation of dims by exp.

    :param dims: The base dimensions.
    :type dims: ``tuple``
    :param exp: The power to raise the base dimensions to.
    :type exp: ``numbers.Real``
    :rtype: ``tuple``
    """
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
    """Express dimensions as a human readable string.

    :param dims: The base unit dimensions to present.
    :type dims: ``tuple``
    :rtype: ``str``
    """
    return "*".join(
        "%s**%g" % (unit_abbreviation, power)
        for unit_abbreviation, power in zip(abbreviations, dims)
        if power != 0
    )


#:
angle_t = SIDimensions()

#:
solid_angle_t = SIDimensions()

#:
strain_t = SIDimensions()

#:
ratio_t = SIDimensions()

#:
mass_t = SIDimensions(kg=1)

#:
distance_t = SIDimensions(m=1)

#:
time_t = SIDimensions(s=1)

#:
temperature_t = SIDimensions(k=1)

#:
current_t = SIDimensions(a=1)

#:
amount_t = SIDimensions(mol=1)

#:
luminosity_t = SIDimensions(cd=1)

#:
frequency_t = SIDimensions(s=-1)

#:
speed_t = dim_div(distance_t, time_t)

#:
acceleration_t = dim_div(speed_t, time_t)

#:
jerk_t = dim_div(acceleration_t, time_t)

#:
jounce_t = dim_div(jerk_t, time_t)

#:
area_t = dim_pow(distance_t, 2)

#:
volume_t = dim_pow(distance_t, 3)

#:
density_t = dim_div(mass_t, volume_t)

#:
volumetric_flow_t = dim_div(volume_t, time_t)

#:
force_t = dim_mul(mass_t, acceleration_t)

#:
moment_t = dim_mul(force_t, distance_t)

#:
torque_t = moment_t

#:
impulse_t = dim_mul(force_t, time_t)

#:
momentum_t = impulse_t

#:
stress_t = dim_div(force_t, area_t)

#:
pressure_t = stress_t

#:
hydrostatic_pressure_t = dim_mul(density_t, dim_mul(acceleration_t, distance_t))

#:
stiffness_t = dim_div(force_t, distance_t)

#:
surface_tension_t = stiffness_t

#:
energy_t = dim_mul(force_t, distance_t)

#:
work_t = energy_t

#:
heat_t = energy_t

#:
power_t = dim_div(energy_t, time_t)

#:
charge_t = dim_mul(current_t, time_t)

#:
potential_t = dim_div(energy_t, current_t)

#:
capacitance_t = dim_div(charge_t, potential_t)

#:
resistance_t = dim_div(potential_t, current_t)

#:
impedance_t = resistance_t

#:
reactance_t = resistance_t

#:
conductance_t = dim_div(current_t, potential_t)

#:
magnetic_flux_t = dim_div(energy_t, current_t)

#:
magnetic_flux_density_t = dim_div(magnetic_flux_t, area_t)

#:
inductance_t = dim_mul(impedance_t, time_t)

#:
luminous_flux_t = dim_mul(luminosity_t, solid_angle_t)

#:
illuminance_t = dim_div(luminous_flux_t, area_t)

#:
molarity_t = dim_div(amount_t, volume_t)

#:
molality_t = dim_div(amount_t, mass_t)

#:
molar_mass_t = dim_div(mass_t, amount_t)

#:
entropy_t = dim_div(energy_t, temperature_t)

#:
heat_capacity_t = entropy_t

#:
specific_entropy_t = dim_div(entropy_t, mass_t)

#:
specific_heat_capacity_t = specific_entropy_t

#:
temperature_gradient_t = dim_div(temperature_t, distance_t)
