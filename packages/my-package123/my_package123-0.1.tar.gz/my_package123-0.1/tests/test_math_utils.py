# test_math_utils.py

import unittest
from my_package123.math_utils import add, subtract, multiply, divide

class TestMathUtils(unittest.TestCase):
    
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
    
    def test_subtract(self):
        self.assertEqual(subtract(5, 3), 2)
    
    def test_multiply(self):
        self.assertEqual(multiply(2, 3), 6)
    
    def test_divide(self):
        self.assertEqual(divide(6, 3), 2)
        with self.assertRaises(ValueError):
            divide(6, 0)

if __name__ == '__main__':
    unittest.main()
