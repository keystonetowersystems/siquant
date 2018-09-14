import unittest

import numpy as np

import siquant.units as u

from siquant import Mass, Distance

class MassTestCase(unittest.TestCase):

    def test_distance(self):

        dist = Distance(1000, u.meters)

        self.assertEqual(dist.get(), 1000)

    def test_mass(self):

        mass = Mass(1000)

        self.assertEqual(mass, Mass(1000, u.kilograms))
        self.assertEqual(mass, Mass(1, u.tonnes))

        self.assertEqual(mass + mass, Mass(2000))
        self.assertEqual(2 * mass, Mass(2000))
        self.assertEqual(mass - mass, Mass(0))
        self.assertEqual(mass / 2, Mass(500))

        self.assertEqual(mass.get_as(u.kilograms), 1000)
        self.assertEqual(mass.get_as(u.tonnes), 1)
        self.assertEqual(mass.get_as(u.grams), 1000000)

        grams = np.array([1000, 2000, 3000])
        masses = Mass(grams, u.grams)

        for (kilos, grams) in zip(masses.get(), grams):
            self.assertEqual(kilos, grams / 1000)



if __name__ == '__main__':
    unittest.main()
