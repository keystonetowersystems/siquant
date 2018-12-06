import sys
import math

from copy import copy, deepcopy

import pytest
import numpy as np

import siquant.dimensions as dims

from siquant.exceptions import UnitMismatchError, ImmutabilityError
from siquant import make, converter, validator, are_of, si, SIUnit


def test_q_copying():
    a = 100 * si.meters
    b = copy(a)
    c = deepcopy(a)

    assert a is not b
    assert a is not c
    assert a == b
    assert a == c

    class Ref:
        def __init__(self, value):
            self.value = value

        def __eq__(self, other):
            return self.value == other.value

    ref = Ref(100)
    ref_ref = Ref(Ref(100))

    rq = make(ref, si.meters)
    rc = copy(rq)

    assert rq == rc
    assert rq is not rc

    rqq = make(ref_ref, si.meters)
    rqc = copy(rqq)
    rqd = deepcopy(rqq)

    assert rqq is not rqc
    assert rqq == rqc

    ref_ref.value.value = 50
    assert rqq == rqc
    assert rqq != rqd


def test_q_immutability():
    mass = 100 * si.kilograms
    with pytest.raises(ImmutabilityError):
        mass.quantity = 10
    with pytest.raises(ImmutabilityError):
        del mass.quantity


def test_q_np():
    distances = make(np.array([1, 2, 3, 4, 5, 6, 7]), si.meters)
    distances *= 2

    value = distances.get_as(si.meters)
    assert np.array_equal(value, np.array([2, 4, 6, 8, 10, 12, 14]))

    assert distances[0].approx(2 * si.meters)
    assert distances[6].approx(14 * si.meters)

    assert min(distances).approx(2 * si.meters)
    assert max(distances).approx(14 * si.meters)


def test_q_round_to():
    distance = 1.23456789 * si.meters

    assert 1235 == distance.round_to(si.millimeters).quantity

    assert 1234.6 == distance.round_to(si.millimeters, 1).quantity


def test_q_approx():

    dist1 = 1.234567890 * si.meters
    dist2 = 1.234567 * si.meters

    assert dist1.approx(dist2)
    assert dist1.approx(dist2, atol=1 * si.millimeters)

    assert dist1.abs_approx(dist2)

    with pytest.raises(UnitMismatchError):
        dist1.approx(dist2, atol=1 * si.milligrams)

    assert not dist1.approx(1.23456789 * si.kilograms)

    dist1 = 1234567890 * si.meters
    dist2 = 1234567891 * si.meters

    assert dist1.approx(dist2)
    assert dist1.rel_approx(dist2)
    assert not dist1.approx(dist2, rtol=0)
    assert not dist1.abs_approx(dist2)

    assert dist1.approx(dist2, rtol=0, atol=1 * si.meters)


@pytest.mark.skipif(
    sys.version_info < (3, 5), reason="operators.matmul introduced in py35"
)
def test_q_matmul():
    from operator import matmul

    distances = make(np.array([1, 2, 3]), si.meters)
    value = matmul(distances, distances)
    assert value.get_as(si.meters ** 2) == 14

    value = matmul(distances, np.array([1, 2, 3]))
    assert value.get_as(si.meters ** 1) == 14

    with pytest.raises(TypeError):
        # numpy really should just return NotImplemented instead of throwing a TypeError
        value = matmul(np.array([1, 2, 3]), distances)
        assert value.get_as(si.meters ** 1) == 14


def test_are_of_validator():
    dim_check = validator(dims.speed_t)

    assert dim_check(1 * si.meters / si.seconds)
    assert dim_check(1 * si.meters / si.seconds, 2 * si.meters / si.seconds)
    assert not dim_check(1 * si.meters)
    assert not dim_check(1)
    assert not dim_check(None)

    with pytest.raises(TypeError):
        validator([1, 2, 3, 4, 5, 6, 7])

    with pytest.raises(ValueError):
        validator((1, 2, 3))


def test_are_of():
    assert are_of(dims.distance_t, 1 * si.meters, 2 * si.millimeters, 3 * si.kilometers)
    assert not are_of(dims.angle_t, 1, 2, 3)
    assert not are_of(dims.distance_t, 1 * si.meters, 1 * si.kilograms)


def test_create_and_extract():
    mass = make(100, SIUnit.Unit(kg=1))
    acceleration = make(1, SIUnit.Unit(m=1, s=-2))

    force = 100 * si.newtons

    assert force.quantity == 100
    assert force.get_as(si.kilonewtons) == 0.1
    assert force == mass * acceleration


def test_hash():
    angle1 = 2 * math.pi * si.radians
    angle2 = 360 * si.degrees

    assert hash(angle1) == hash(angle2)

    circumference = angle1 * 1 * si.meters
    assert hash(circumference) != hash(angle1)


def test_q_compatible():
    dist1 = 1 * si.meters
    dist2 = 1 * si.millimeters
    area = 1 * si.meters ** 2
    assert dist1.compatible(dist2)
    assert dist2.compatible(dist1)
    assert not dist1.compatible(area)
    assert not area.compatible(dist1)

    with pytest.raises(TypeError):
        dist = 1 * si.meters
        dist.compatible(si.meters)


def test_q_eq_ne():
    dist1 = 1 * si.meters
    dist2 = 1000 * si.millimeters
    dist3 = 1 * si.kilometers
    area = 1 * si.meters ** 2

    assert dist1 == dist2
    assert dist2 == dist1

    assert dist1 != 1
    assert dist2 != 1000
    assert area != 1

    assert dist1 != dist3
    assert dist3 != dist1

    assert not area == dist1
    assert not dist1 == area

    assert not dist1 == si.meters
    assert not si.meters == dist1

    assert area != dist1
    assert dist1 != area

    assert dist1 != si.meters
    assert si.meters != dist1

    count = 500 * si.unity

    assert dist1 != count
    assert count != dist1

    assert count == 500 * si.unity
    assert count == 500
    assert 500 == count

    percent = SIUnit.Unit(1 / 100)

    hundo = 100 * percent

    assert hundo == 1


def test_q_ordering():
    dist1 = 1 * si.meters
    dist2 = 1000 * si.millimeters
    dist3 = 1 * si.kilometers
    dist4 = 1 * si.millimeters
    area = 1 * si.meters ** 2

    assert dist1 >= dist2
    assert dist2 <= dist1
    assert dist1 <= dist2
    assert dist2 >= dist1

    assert dist3 >= dist1
    assert dist1 <= dist3
    assert dist3 > dist1
    assert dist1 < dist3

    assert dist4 <= dist1
    assert dist1 >= dist4
    assert dist4 < dist1
    assert dist1 > dist4

    with pytest.raises(UnitMismatchError):
        dist1 > area
    with pytest.raises(UnitMismatchError):
        dist1 >= area
    with pytest.raises(UnitMismatchError):
        dist1 < area
    with pytest.raises(UnitMismatchError):
        dist1 <= area

    with pytest.raises(TypeError):
        dist1 > 1
    with pytest.raises(TypeError):
        dist1 >= 1
    with pytest.raises(TypeError):
        dist1 < 1
    with pytest.raises(TypeError):
        dist1 <= 1


def test_q_float():
    assert pytest.approx(1) == math.cos(0 * si.radians)
    assert pytest.approx(-1) == math.cos(math.pi * si.radians)
    assert pytest.approx(0) == math.cos(math.pi / 2 * si.radians)
    assert pytest.approx(0) == math.cos(math.pi * 3 / 2 * si.radians)


def test_q_truth():
    dist_true = 1 * si.meters
    dist_false = 0 * si.meters
    assert dist_true
    assert not dist_false


def test_q_abs():
    assert abs(1 * si.meters) == 1 * si.meters
    assert abs(-1 * si.meters) == 1 * si.meters


def test_q_invert():
    dist = 1000 * si.millimeters
    assert ~dist == 1 / 1000 / si.millimeters


def test_q_neg():
    dist = 1000 * si.millimeters
    assert -dist == -1000 * si.millimeters


def test_q_pow():
    dist = 1000 * si.millimeters
    assert dist ** 2 == 1 * si.meters ** 2
    assert dist ** -1 == 1 * si.meters ** -1

    dist = 100 * si.millimeters ** 2
    assert dist ** 0.5 == 10 * si.millimeters

    with pytest.raises(TypeError):
        dist ** dist
    with pytest.raises(TypeError):
        dist ** si.meters


def test_q_mul():
    dist = 1000 * si.millimeters
    assert 2 * dist == 2000 * si.millimeters
    assert dist * 2 == 2000 * si.millimeters
    assert dist * dist == 1000 * 1000 * si.millimeters ** 2

    dist *= 2
    assert dist == 2000 * si.millimeters


def test_q_div():
    dist = 1000 * si.millimeters
    assert 2 / dist == 1 / 500 / si.millimeters
    assert dist / 2 == 500 * si.millimeters
    assert dist / dist == 1 * si.unity

    assert dist / si.millimeters == 1000 * si.unity
    assert si.millimeters / dist == 1 / 1000 * si.unity

    with pytest.raises(TypeError):
        dist / (1, 2)
    with pytest.raises(TypeError):
        (1, 2) / dist


def test_dimensionality():
    dist = 1000 * si.millimeters
    assert dist.is_of(dims.distance_t)
    assert not dist.is_of(dims.area_t)


def test_q_add():
    dist1 = 1 * si.meters
    dist2 = 1000 * si.millimeters
    area = dist1 * dist2

    diff1 = dist1 + dist2
    diff2 = dist2 + dist1

    assert diff1 == 2 * si.meters
    assert diff1.units == si.meters

    assert diff2 == 2 * si.meters
    assert diff2.units == si.millimeters

    with pytest.raises(TypeError):
        dist1 + si.meters
    with pytest.raises(TypeError):
        si.meters + dist1

    with pytest.raises(UnitMismatchError):
        dist1 + area
    with pytest.raises(UnitMismatchError):
        area + dist1

    dist1 += dist2
    assert dist1 == 2 * si.meters

    count = 100 * si.unity
    assert count == 100
    assert count + 100 == 200


def test_q_sub():
    dist1 = 1 * si.meters
    dist2 = 1000 * si.millimeters
    area = dist1 * dist2

    diff1 = dist1 - dist2
    diff2 = dist2 - dist1

    assert diff1 == 0 * si.meters
    assert diff1.units == si.meters

    assert diff2 == 0 * si.meters
    assert diff2.units == si.millimeters

    with pytest.raises(TypeError):
        dist1 - si.meters
    with pytest.raises(TypeError):
        si.meters - dist1

    with pytest.raises(UnitMismatchError):
        dist1 - area
    with pytest.raises(UnitMismatchError):
        area - dist1

    dist1 -= dist2
    assert dist1 == 0 * si.meters

    count = 500 * si.unity
    assert count == 500 * si.unity
    assert count - 100 == 400 * si.unity
    assert count - 100 == 400
    assert 1000 - count == 500 * si.unity
    assert 1000 - count == 500


def test_q_converters():
    cvtr = converter(si.meters)
    assert cvtr(1000) == 1000 * si.meters
    assert cvtr(1000 * si.meters) == 1000 * si.meters
    assert cvtr(1000 * si.millimeters) == 1 * si.meters

    with pytest.raises(UnitMismatchError):
        cvtr(1000 * si.kilograms)
