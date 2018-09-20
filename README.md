# siquant

A library to provide dimensional and quantitative analysis within the SI units system.

# Description

This library provides a reasonably efficient set of tools to easily track units through abitrary calculations. All types
are designed to be immutable, and as such can be shared relatively freely.

There are two primary data types:
* SIUnit - provide some scaling factor of a specific dimensionality of the 7 fundamental SI units.
* ScalarQuantity - support arithmetic of a quantity of units

Some predefined units are provided in modules in the siquant.systems package.

# Getting Started

```python
>>>from siquant.systems import si
>>>force = 100 * si.kilonewtons
>>>moment_arm = 50 * si.meters
>>>torque = force * moment_arm
>>>torque.get()
5000
>>>str(torque.units)
'1000*kg**1*m**2*s**-2'
>>>torque.get_as(si.newtons * si.meters)
5000000.0
>>>torque.get_as(si.newtons)
Traceback (most recent call last):
  File "<input>", line 1, in <module>
  File "/siquant/siquant/quantities.py", line 19, in get_as
      assert(self._units.compatible(units))
AssertionError
>>>torque = torque.normalized()
>>>torget.get()
5000000.0
>>>str(torque.units)
'1*kg**1*m**2*s**-2'
```

# Defining New Units

New unit types can be created:
* implicitly derived through combination of existing units.
* explicitly via the Unit.Unit() factory method.

## Derived Units  

```python
from siquant.systems import si
pounds = si.kilograms * si.SIUnit.Unit(0.445)
inches = si.millimeters * si.SIUnit.Unit(25.4)
ksi = si.kilo * pounds / inches ** 2
```

## Explicit Units

```python
from siquant.systems import si
from siquant.units import SIUnit
wonky_pi_unit = SIUnit.Unit(3.14, m=1)
circle = 100 * wonky_pi_unit
diameter = circle.get()
circumeference = circle.get_as(si.meters)
``` 

# Supporting Vector Quantities

There are a number of vector libraries available, all with different interfaces. As such, a ```VectorQuantity``` is not 
provided. However, integration of existing vector libraries should be possible with relative ease.

## Provide a VectorQuantity interface:

```python
import numbers
from siquant.quantities import Quantity, ScalarQuantity

class VectorQuantity(Quantity):
    
    def cross(self, other):
        if not isinstance(other, VectorQuantity):
            raise TypeError()
        return VectorQuantity(self.quantity.cross(other.quantity), self.units * other.units)
        
    def dot(self, other):
        if not isinstance(other, VectorQuantity):
            raise TypeError()
        return ScalarQuantity(self.quantity.dot(other.quantity), self.units * other.units)
        
    def __mul__(self, other):
        if isinstance(other, numbers.Real):
            return VectorQuantity(self.quantity * other, self.units)
        if isinstance(other, ScalarQuantity):
            return VectorQuantity(self.quantity * other.quantity, self.units * other.units)
        if isinstance(other, VectorQuantity):
            return self.dot(other)
        return NotImplemented
        
    def __rmul__(self, other):
        # Real, ScalarQuantity
        ...
        
    # etc ...
    
force_vector = VectorQuantity(my_vector, si.newtons)
```

## Provide a hook for SIUnit (optional)

The arithmetic methods of ```SIUnit``` only support operands of type ```numbers.Real``` and ```SIUnit```. In all other
cases NotImplemented is returned. The interpretter will then attempt to delegate that operation to the other operand 
type.

In order to support the behavior ```Vector * SIUnit -> VectorQuantity``` the special methods ```__mul__``` and 
```__rmul__``` should be augmented. The exact implementation will depend heavily upon the library being integrated, 
in order to make sure that the new child type is always propagated correctly.

### Composition

```python
from siquant.units import SIUnit
from your.vec.lib import Vector

class VectorWrapper:
    
    @classmethod
    def Make(cls, *args, **kwargs):
        return cls(Vector(*args, **kwargs))

    def __init__(self, vector):
        self._vector = vector

    def unwrap(self):
        return self._vector

    def __mul__(self, other):
        if isinstance(other, SIUnit):
            return VectorQuantity(self, other)
        return VectorWrapper(self._vector * other)
        
    def __rmul__(self, other):
        if isinstance(other, SIUnit):
            return VectorQuantity(self, other)
        return VectorWrapper(other * self._vector)
        
    # any other operations to support
```

### Inheritance

```python
from siquant.units import SIUnit
from your.vec.lib import Vector

class QVector(Vector):
    
    def __mul__(self, other):
        if isinstance(other, SIUnit):
            return VectorQuantity(self, other)
        return super().__mul__(other)
        
    __rmul__ = __imul__ = __mul__
```
### Including siquant as a dependency

This is probably the simplest, and the least practical. 