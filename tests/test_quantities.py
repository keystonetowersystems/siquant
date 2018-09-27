from siquant.units import SIUnit
from siquant.quantities import ScalarQuantity
from siquant.systems import si

def test_create_and_extract():
    mass = ScalarQuantity(100, SIUnit.Unit(kg=1))
    acceleration = ScalarQuantity(1, SIUnit.Unit(m=1, s=-2))

    force = 100 * si.newtons

    assert force.get() == 100
    assert force.get_as(si.kilonewtons) == 0.1
    assert force == mass * acceleration

def test_q_pow():
    pass

def test_q_mul():
    pass

def test_q_div():
    pass

def test_q_add():
    pass

def test_q_sub():
    pass

def test_q_converters():
    pass
