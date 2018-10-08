from typing import Tuple

# Technically any type that implements numbers.Real will work;
# I'm not really sure how to make that work with mypy though.

Dimensions = Tuple[float, float, float, float, float, float, float]

def SIDimensions(
    kg: float = 0,
    m: float = 0,
    s: float = 0,
    k: float = 0,
    a: float = 0,
    mol: float = 0,
    cd: float = 0,
) -> Dimensions: ...
def dim_mul(dim1: Dimensions, dim2: Dimensions) -> Dimensions: ...
def dim_div(dim1: Dimensions, dim2: Dimensions) -> Dimensions: ...
def dim_pow(dim1: Dimensions, exp: float) -> Dimensions: ...
def dim_str(dim: Dimensions) -> str: ...

angle_t: Dimensions
solid_angle_t: Dimensions
strain_t: Dimensions
ratio_t: Dimensions
mass_t: Dimensions
distance_t: Dimensions
time_t: Dimensions
temperature_t: Dimensions
current_t: Dimensions
amount_t: Dimensions
luminosity_t: Dimensions
frequency_t: Dimensions

speed_t: Dimensions
acceleration_t: Dimensions
jerk_t: Dimensions
jounce_t: Dimensions

area_t: Dimensions
volume_t: Dimensions

density_t: Dimensions
volumetric_flow_t: Dimensions

force_t: Dimensions
impulse_t: Dimensions
momentum_t: Dimensions
pressure_t: Dimensions
stress_t: Dimensions
hydrostatic_pressure_t: Dimensions
surface_tension_t: Dimensions
stiffness_t: Dimensions

energy_t: Dimensions
work_t: Dimensions
heat_t: Dimensions
power_t: Dimensions

charge_t: Dimensions
potential_t: Dimensions
capacitance_: Dimensions
resistance_: Dimensions
impedance_t: Dimensions
reactance_t: Dimensions
conductance_t: Dimensions
magnetic_flux_t: Dimensions
magnetic_flux_density_t: Dimensions
inductance_t: Dimensions
luminous_flux_t: Dimensions
illuminance_t: Dimensions

molarity_t: Dimensions
molality_t: Dimensions
molar_mass_t: Dimensions

entropy_t: Dimensions
heat_capacity_t: Dimensions
specific_entropy_t: Dimensions
specific_heat_capacity_t: Dimensions
temperature_gradient_t: Dimensions
