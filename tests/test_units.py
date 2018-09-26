import unittest

from siquant.units import SIUnit

class UnitTypeTestCase(unittest.TestCase):

    def test_create_meters(self):
        m = SIUnit.Unit(m=1)
        self.assertEqual(m.scale, 1)
        self.assertEqual(m.m, 1)
        self.assertEqual(m.kg, 0)
        self.assertEqual(m.s, 0)
        self.assertEqual(m.mol, 0)
        self.assertEqual(m.a, 0)
        self.assertEqual(m.k, 0)
        self.assertEqual(m.cd, 0)

    def test_create_unitless(self):
        pi = SIUnit.Unit(3.14159)
        self.assertEqual(pi.scale, 3.14159)
        self.assertEqual(pi.m, 0)
        self.assertEqual(pi.kg, 0)
        self.assertEqual(pi.s, 0)
        self.assertEqual(pi.mol, 0)
        self.assertEqual(pi.a, 0)
        self.assertEqual(pi.k, 0)
        self.assertEqual(pi.cd, 0)

    def test_create_kg(self):
        kg = SIUnit.Unit(kg=1)
        self.assertEqual(kg.scale, 1)
        self.assertEqual(kg.m, 0)
        self.assertEqual(kg.kg, 1)
        self.assertEqual(kg.s, 0)
        self.assertEqual(kg.mol, 0)
        self.assertEqual(kg.a, 0)
        self.assertEqual(kg.k, 0)
        self.assertEqual(kg.cd, 0)

    def test_create_s(self):
        s = SIUnit.Unit(s=1)
        self.assertEqual(s.scale, 1)
        self.assertEqual(s.m, 0)
        self.assertEqual(s.kg, 0)
        self.assertEqual(s.s, 1)
        self.assertEqual(s.mol, 0)
        self.assertEqual(s.a, 0)
        self.assertEqual(s.k, 0)
        self.assertEqual(s.cd, 0)

    def test_create_mol(self):
        pass

    def test_create_a(self):
        pass

    def test_create_k(self):
        pass

    def test_create_cd(self):
        pass

    def test_mul_div_unit(self):
        m = SIUnit.Unit(m=1)
        speed = m / SIUnit.Unit(s=1)
        self.assertEqual(speed.m, 1)
        self.assertEqual(speed.s, -1)

        mm = m / SIUnit.Unit(1000)
        self.assertEqual(mm.scale, 1 / 1000)
        self.assertEqual(mm.m, 1)

        self.assertEqual(m, SIUnit.Unit(1000) * mm)

    def test_pow_unit(self):
        pass

    def test_eq_unit(self):
        pass

    def test_compatible_unit(self):
        pass

    def test_base_units(self):
        pass