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

# Extending Quantity Conversions

Quantities are restricted to only allow operations with operands of types where 
an explicit conversion function has been registered.

```python
>>> Moment(1) / SectionModulus(1)
Stress(1.000000, units=Unit(1.000000, m=-1, kg=1, s=-2, k=0, amp=0, cd=0, mol=0))

# Even though Volume has the same base_units as SectionModulus,
# only explicitly provided operations should succeed.

>>> Moment(1) / Volume(1)
Traceback (most recent call last):
  File "<input>", line 1, in <module>
  File "/siquant/siquant/quantities/dispatch.py", line 5, in dispatch
    fcn = registry[type(other)]
KeyError: <class 'siquant.quantities.qtypes.Volume'>
```

See [operations.py](siquant/quantities/operations.py)

### Adding User Defined Operations 

```python
import numpy as np
import siquant.quantities as q

def force_times_distance(force, distance):
    return q.Moment(force.get() * distance.get())

q.Force.multiplier(q.Distance)(force_times_distance)

def force_vector(force, ndarray_instance):
    return q.Force(force.get() * ndarray_instance)
    
q.Force.multiplier(np.ndarray)(force_vector)

```

A short hand is also provided if both the operand and the result have class type Quantity,
and base_units with factor=1.

```python
q.Force.q_multiplier(q.Distance, q.Moment)

# is equivalent to:

def force_times_distance(force, distance):
    return q.Moment(
        force.get() * distance.get(), 
        units=force.base_units * distance.base_units
    )
q.Force.multiplier(q.Distance)(force_times_distance)
```

Note that this does induce some overhead for unit conversion with the quantity conversion.

### Adding User Defined Quantities

```python
import siquant.units as u
import siquant.quantities as q
from siquant.quantities.meta import LinearQuantity

percentage = u.Unit(1 / 100)

class Efficiency(metaclass=LinearQuantity, base_units=u.unity):
    pass
    
test = Efficiency(90, units=percentage)
test.get() # 0.9
test.get_as(percentage) # => 90.0

Efficiency.q_multiplier(q.Power, q.Power)
```