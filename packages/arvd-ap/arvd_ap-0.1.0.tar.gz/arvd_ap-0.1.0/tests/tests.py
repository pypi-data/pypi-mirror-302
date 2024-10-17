# tests/test_your_code.py

import unittest
from arvd_ap import rvd_ap

class TestYourCode(unittest.TestCase):
    def test_some_function(self):
        result = arvd_ap.some_function()
        self.assertEqual(result, expected_result)

    def test_some_class(self):
        obj = arvd_ap.SomeClass()
        self.assertTrue(obj.some_method())

if __name__ == '__main__':
    unittest.main()
