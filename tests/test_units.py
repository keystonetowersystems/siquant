import pytest

from siquant.units import SIUnit, ScalarQuantity

@pytest.fixture
def unit():
    return SIUnit.Unit(scale=10, kg=1, m=2, s=3, k=4, a=5, mol=6, cd=7)

def test_unit_create():
    with pytest.raises(ValueError):
        SIUnit.Unit(0, kg=1, m=2, s=3, k=4, a=5, mol=6, cd=7)
    with pytest.raises(ValueError):
        SIUnit.Unit(-1, kg=1, m=2, s=3, k=4, a=5, mol=6, cd=7)

def test_hash(unit):

    other_scale = SIUnit(1, unit.dimensions)
    assert hash(unit) != hash(other_scale)
    assert hash(unit) == hash(SIUnit.Unit(10) * other_scale)

    other_dims = SIUnit.Unit(10)
    assert hash(unit) != other_dims


def test_unit_accessors(unit):
    assert unit.scale == 10
    assert unit.kg == 1
    assert unit.m == 2
    assert unit.s == 3
    assert unit.k == 4
    assert unit.a == 5
    assert unit.mol == 6
    assert unit.cd == 7


def test_unit_cmp(unit):
    assert unit == unit
    assert unit != SIUnit.Unit()

    assert not unit == object()
    assert unit != object()

def test_unit_mul(unit):
    original_dimensions = unit.dimensions

    assert unit * SIUnit.Unit(2) == SIUnit(20.0, original_dimensions)
    assert SIUnit.Unit(2) * unit == SIUnit(20.0, original_dimensions)
    assert unit * unit == SIUnit.Unit(100.0, kg=2, m=4, s=6, k=8, a=10, mol=12, cd=14)

    assert 2 * unit == ScalarQuantity(2, unit)
    assert unit * 2 == ScalarQuantity(2, unit)

    assert 2 * unit * unit == ScalarQuantity(2, unit * unit)
    assert unit * (2 * unit) == ScalarQuantity(2, unit * unit)

    unit2 = unit
    unit2 *= unit2
    assert unit2 == unit * unit

    with pytest.raises(TypeError):
        unit * None
    with pytest.raises(TypeError):
        None * unit
    with pytest.raises(TypeError):
        unit *= None

def test_unit_div(unit):
    original_dimensions = unit.dimensions
    inverted_unit = SIUnit.Unit(1 / 10, kg=-1, m=-2, s=-3, k=-4, a=-5, mol=-6, cd=-7)
    assert unit / SIUnit.Unit(2) == SIUnit(5, original_dimensions)
    assert SIUnit.Unit(2) / unit == SIUnit(2 / 10, inverted_unit._dimensions)
    assert unit / unit == SIUnit.Unit(1)

    assert 2 / unit == ScalarQuantity(2, inverted_unit)
    assert unit / 2 == ScalarQuantity(1 / 2, unit)

    assert unit / 2 / unit == ScalarQuantity(1 / 2, SIUnit.Unit(1))
    assert unit / (2 / unit) == ScalarQuantity(50, SIUnit.Unit(1, 2, 4, 6, 8, 10, 12, 14))

    unit /= unit
    assert unit == SIUnit.Unit(1)

    with pytest.raises(TypeError):
        unit / None
    with pytest.raises(TypeError):
        None / unit
    with pytest.raises(TypeError):
        unit /= None

def test_unit_base_units(unit):
    assert unit.base_units() == unit / SIUnit.Unit(unit.scale)

def test_unit_pow(unit):
    assert unit ** 2 == unit * unit
    assert unit ** 3 == unit * unit * unit
    assert unit ** -1 == SIUnit.Unit(1) / unit
    assert unit ** -2 == SIUnit.Unit(1) / unit / unit

    with pytest.raises(TypeError):
        unit = unit ** unit

def test_unit_invert(unit):
    assert ~unit == SIUnit.Unit(1 / 10, kg=-1, m=-2, s=-3, k=-4, a=-5, mol=-6, cd=-7)

def test_unit_compatible(unit):
    assert unit.compatible(unit)
    assert unit.compatible(SIUnit.Unit(2) * unit)
    assert not unit.compatible(unit * unit)
    assert not unit.compatible(SIUnit.Unit(1))
