from siquant.units import SIUnit


def test_create_meters():
    m = SIUnit.Unit(m=1)
    assert m.scale == 1
    assert m.m == 1
    assert m.kg == 0
    assert m.s == 0
    assert m.mol == 0
    assert m.a == 0
    assert m.k == 0
    assert m.cd == 0


def test_create_unitless():
    pi = SIUnit.Unit(3.14159)
    assert pi.scale == 3.14159
    assert pi.m == 0
    assert pi.kg == 0
    assert pi.s == 0
    assert pi.mol == 0
    assert pi.a == 0
    assert pi.k == 0
    assert pi.cd == 0


def test_create_kg():
    kg = SIUnit.Unit(kg=1)
    assert kg.scale == 1
    assert kg.m == 0
    assert kg.kg == 1
    assert kg.s == 0
    assert kg.mol == 0
    assert kg.a == 0
    assert kg.k == 0
    assert kg.cd == 0


def test_create_s():
    s = SIUnit.Unit(s=1)
    assert s.scale == 1
    assert s.m == 0
    assert s.kg == 0
    assert s.s == 1
    assert s.mol == 0
    assert s.a == 0
    assert s.k == 0
    assert s.cd == 0


def test_create_mol():
    pass


def test_create_a():
    pass


def test_create_k():
    pass


def test_create_cd():
    pass


def test_mul_div_unit():
    m = SIUnit.Unit(m=1)
    speed = m / SIUnit.Unit(s=1)
    assert speed.m == 1
    assert speed.s == -1

    mm = m / SIUnit.Unit(1000)
    assert mm.scale == 1 / 1000
    assert mm.m == 1

    assert m == SIUnit.Unit(1000) * mm


def test_pow_unit():
    pass


def test_eq_unit():
    pass


def test_compatible_unit():
    pass


def test_base_units():
    pass
