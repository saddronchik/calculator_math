import unittest
import math
from calculator import ScientificCalculator  # если вынесена логика

class TestScientificCalculator(unittest.TestCase):
    
    def test_addition(self):
        self.assertEqual(eval("2 + 2"), 4)
        self.assertEqual(eval("10.5 + 5.5"), 16)
    
    def test_multiplication(self):
        self.assertEqual(eval("6 * 7"), 42)
    
    def test_scientific_functions(self):
        self.assertAlmostEqual(math.sin(math.radians(30)), 0.5, places=5)
        self.assertAlmostEqual(math.sqrt(16), 4.0, places=5)
        self.assertAlmostEqual(math.log10(100), 2.0, places=5)
    
    def test_power(self):
        self.assertEqual(eval("2 ** 8"), 256)
    
    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            eval("10 / 0")

if __name__ == '__main__':
    unittest.main()