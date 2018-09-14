import unittest

import siquant.units as u

class BaseUnitTestCase(unittest.TestCase):

    def test_base_units_at_unity(self):

        self.assertEqual(u.meters.factor, 1)
        self.assertEqual(u.square_meters.factor, 1)
        self.assertEqual(u.cubic_meters.factor, 1)
        self.assertEqual(u.quartic_meters.factor, 1)
        self.assertEqual(u.kilograms.factor, 1)
        self.assertEqual(u.seconds.factor, 1)
        self.assertEqual(u.newtons.factor, 1)
        self.assertEqual(u.newton_meters.factor, 1)
        self.assertEqual(u.pascals.factor, 1)
        self.assertEqual(u.hertz.factor, 1)
        self.assertEqual(u.radians.factor, 1)

    def test_distance_units(self):

        self.assertTrue(u.meters.matches_dimensions(u.meters))
        self.assertTrue(u.millimeters.matches_dimensions(u.meters))
        self.assertTrue(u.centimeters.matches_dimensions(u.meters))

        self.assertFalse(u.square_meters.matches_dimensions(u.meters))
        self.assertFalse(u.cubic_meters.matches_dimensions(u.meters))
        self.assertFalse(u.quartic_meters.matches_dimensions(u.meters))

        self.assertFalse(u.seconds.matches_dimensions(u.meters))
        self.assertFalse(u.kilograms.matches_dimensions(u.meters))

        self.assertFalse(u.newtons.matches_dimensions(u.meters))
        self.assertFalse(u.newton_meters.matches_dimensions(u.meters))

        self.assertEqual(u.meters.scale(100), 100)
        self.assertEqual(u.millimeters.scale(100), 100000)
        self.assertEqual(u.centimeters.scale(100), 10000)

    def test_area_units(self):

        self.assertTrue(u.square_meters.matches_dimensions(u.square_meters))
        self.assertTrue(u.square_centimeters.matches_dimensions(u.square_meters))
        self.assertTrue(u.square_millimeters.matches_dimensions(u.square_meters))






if __name__ == '__main__':
    unittest.main()
