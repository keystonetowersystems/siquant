import unittest

import siquant.dimensions as d

class DimensionTestCase(unittest.TestCase):

    def test_dim_mul(self):
        m = d.SIDimensions(kg=1)
        a = d.SIDimensions(m=1, s=-2)

        f = d.dim_mul(m, a)
        self.assertEqual(f, d.SIDimensions(kg=1, m=1, s=-2))

        dist = d.SIDimensions(m=1)
        torque = d.dim_mul(f, dist)
        self.assertEqual(torque, d.SIDimensions(kg=1, m=2, s=-2))

    def test_dim_div(self):

        a = d.SIDimensions(m=1, s=-2)
        f = d.SIDimensions(kg=1, m=1, s=-2)

        m = d.dim_div(f, a)
        self.assertEqual(m, d.SIDimensions(kg=1))

        self.assertEqual(d.dim_div(m, m), d.SIDimensions())

    def test_dim_pow(self):

        dist = d.SIDimensions(m=1)
        area = d.dim_pow(dist, 2)
        self.assertEqual(area, d.SIDimensions(m=2))

        sqrt = d.dim_pow(area, 0.5)
        self.assertEqual(sqrt, d.SIDimensions(m=1))


        v = d.dim_pow(dist, 3)
        self.assertEqual(v, d.SIDimensions(m=3))


if __name__ == '__main__':
    unittest.main()
