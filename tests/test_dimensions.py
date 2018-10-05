import siquant.dimensions as d


def test_create():
    dims = d.SIDimensions(kg=1, m=2, s=3, k=4, a=5, mol=6, cd=7)
    assert dims == (1, 2, 3, 4, 5, 6, 7)


def test_dim_mul():
    m = d.SIDimensions(kg=1)
    a = d.SIDimensions(m=1, s=-2)
    f = d.dim_mul(m, a)
    assert f == d.SIDimensions(kg=1, m=1, s=-2)

    dist = d.SIDimensions(m=1)
    torque = d.dim_mul(f, dist)
    assert torque == d.SIDimensions(kg=1, m=2, s=-2)


def test_dim_div():
    a = d.SIDimensions(m=1, s=-2)
    f = d.SIDimensions(kg=1, m=1, s=-2)
    m = d.dim_div(f, a)
    assert m == d.SIDimensions(kg=1)

    assert d.dim_div(m, m) == d.SIDimensions()


def test_dim_pow():
    dist = d.SIDimensions(m=1)
    area = d.dim_pow(dist, 2)
    assert area == d.SIDimensions(m=2)

    sqrt = d.dim_pow(area, 0.5)
    assert sqrt == d.SIDimensions(m=1)

    v = d.dim_pow(dist, 3)
    assert v == d.SIDimensions(m=3)


def test_dim_to_str():
    s = d.dim_str(d.SIDimensions(kg=1, m=1, s=-2))
    assert s == "kg**1*m**1*s**-2"
