# siquant

A library to provide dimensional and quantitative analysis using the SI units system.

# Description

todo: long description

# Examples

```python
import siquant.quantities as q
import siquant.units as u

force = q.Force(120, u.kilonewtons)
moment = force * q.Distance(100, u.meters)
inertia = q.MomentOfArea(1000000, u.quartic_millimeters)
extreme_fiber = q.Distance(250, u.millimeters)
section_modulus = inertia / extreme_fiber
stress = moment / section_modulus

print(stress.get_as(u.gigapascals))
# 3000 GPa
```