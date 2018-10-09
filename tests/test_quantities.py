import sys
import math

import pytest
import numpy as np

import siquant.dimensions as dims

from siquant.exceptions import UnitMismatchError, ImmutabilityError
from siquant import make, converter, is_of, si, SIUnit


def test_immutability():
    mass = 100 * si.kilograms
    with pytest.raises(ImmutabilityError):
        mass.quantity = 10
    with pytest.raises(ImmutabilityError):
        del mass.quantity


def test_np_quantity():
    distances = make(np.array([1, 2, 3, 4, 5, 6, 7]), si.meters)
    distances *= 2

    value = distances.get_as(si.meters)
    assert np.array_equal(value, np.array([2, 4, 6, 8, 10, 12, 14]))


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


def test_is_of_validator():
    validator = is_of(dims.speed_t)

    assert validator(1 * si.meters / si.seconds)
    assert not validator(1 * si.meters)
    assert not validator(1)
    assert not validator(None)

    with pytest.raises(TypeError):
        is_of([1, 2, 3, 4, 5, 6, 7])

    with pytest.raises(ValueError):
        is_of((1, 2, 3))


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


def test_q_converters():
    cvtr = converter(si.meters)
    assert cvtr(1000) == 1000 * si.meters
    assert cvtr(1000 * si.meters) == 1000 * si.meters
    assert cvtr(1000 * si.millimeters) == 1 * si.meters

    with pytest.raises(UnitMismatchError):
        cvtr(1000 * si.kilograms)
