from siquant.quantities.qtypes import (
    Distance,
    Area,
    Volume,
    Time,
    Velocity,
    Acceleration,
    Mass,
    Density,
    Force,
    Moment,
    Stress,
    MomentOfArea,
    SectionModulus,
    Angle
)

Distance.q_multiplier(Distance, Area)
Distance.q_multiplier(Area, Volume)
Distance.q_multiplier(Force, Moment)
Distance.q_divider(Time, Velocity)

Area.q_multiplier(Distance, Volume)
Area.q_divider(Distance, Distance)

Volume.q_multiplier(Density, Mass)
Volume.q_divider(Distance, Area)
Volume.q_divider(Area, Distance)

Velocity.q_multiplier(Time, Distance)
Velocity.q_divider(Time, Acceleration)

Force.q_multiplier(Distance, Moment)
Force.q_divider(Area, Stress)
Force.q_divider(Stress, Area)

Mass.q_divider(Volume, Density)
Mass.q_multiplier(Acceleration, Force)

Density.q_multiplier(Volume, Mass)

Moment.q_divider(Distance, Force)
Moment.q_divider(Force, Distance)
Moment.q_divider(SectionModulus, Stress)

Stress.q_multiplier(Area, Force)

MomentOfArea.q_divider(Distance, SectionModulus)

Angle.q_multiplier(Distance, Distance)