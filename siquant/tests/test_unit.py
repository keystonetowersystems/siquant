import unittest

from siquant.units import Unit

class UnitsTestCase(unittest.TestCase):

    def test_base_unit_multiply(self):
        kg = Unit(1, kg=1)
        self.assertEqual(kg * kg * kg, Unit(1, kg=3))

        m = Unit(1, m=1)
        self.assertEqual(kg * m, Unit(1, kg=1, m=1))

        s = Unit(1, s=1)
        self.assertEqual(kg * m * s, Unit(1, kg=1, s=1, m=1))


    def test_base_unit_divide(self):
        unity = Unit(1)
        kg = Unit(1, kg=1)
        m = Unit(1, m=1)
        s = Unit(1, s=1)

        self.assertEqual(kg / kg, unity)
        self.assertEqual(m / m, unity)
        self.assertEqual(s / s, unity)

        self.assertEqual(m / s, Unit(1, m=1, s=-1))

    def test_base_unit_pow(self):
        m = Unit(1, m=1)

        self.assertEqual(m ** 3, Unit(1, m=3))

        s = Unit(1, s=1)

        v = m / s
        self.assertEqual(v ** 2, Unit(1, m=2, s=-2))

    def test_normalize(self):

        m = Unit(1, m=1)
        self.assertEqual(m.normalize(100), 100)

        mm = Unit(1 / 1000, m=1)
        self.assertEqual(mm.normalize(100), 0.1)

        km = Unit(1000, m=1)
        self.assertEqual(km.normalize(100), 100000)

        mm_m = mm * m
        self.assertEqual(mm_m.normalize(100), 0.1)