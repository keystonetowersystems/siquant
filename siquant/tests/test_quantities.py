import unittest

import numpy as np

from siquant.units import SIUnit
from siquant.quantities import ScalarQuantity
from siquant.systems import si


class ScalarQuantityTestCase(unittest.TestCase):

    def test_create_and_extract(self):
        mass = ScalarQuantity(100, SIUnit.Unit(kg=1))
        acceleration = ScalarQuantity(1, SIUnit.Unit(m=1, s=-2))

        force = 100 * si.newtons

        self.assertEqual(force.get(), 100)
        self.assertEqual(force.get_as(si.kilonewtons), 0.1)
        self.assertEqual(force, mass * acceleration)

    def test_q_pow(self):
        pass

    def test_q_mul(self):
        pass

    def test_q_div(self):
        pass

    def test_q_add(self):
        pass

    def test_q_sub(self):
        pass