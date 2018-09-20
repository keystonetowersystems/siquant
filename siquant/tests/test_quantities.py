import unittest

import numpy as np

from siquant.quantities import Quantity
from siquant.systems.si import *

from siquant.vector import V2

class ScalarQuantityTestCase(unittest.TestCase):
    pass

class VectorQuantityTestCase(unittest.TestCase):
    pass

class NumpyQuantityTestCase(unittest.TestCase):

    def assertArrayEqual(self, actual, expected):
        for a, e in zip(actual, expected):
            self.assertEqual(a, e)

    def test_create_and_extract(self):

        np_array = np.array([1,2,3,4,5])
        force_vector = Quantity(np_array, newtons)

        self.assertArrayEqual(force_vector.get(), np_array)
        self.assertArrayEqual(force_vector.get_as(kilonewtons), np_array / 1000)

        kn_vector = force_vector.cvt_to(kilonewtons)
        self.assertEqual(type(kn_vector), Quantity)
        self.assertEqual(kn_vector.units, kilonewtons)
        self.assertArrayEqual(kn_vector.get(), np_array / 1000)

        self.assertEqual(force_vector, kn_vector)

