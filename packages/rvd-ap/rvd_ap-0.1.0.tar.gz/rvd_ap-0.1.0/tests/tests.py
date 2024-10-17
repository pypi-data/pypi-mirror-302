# tests/test_your_code.py

import unittest
from rvd_ap import rvd_ap

class TestYourCode(unittest.TestCase):
    def test_some_function(self):
        result = rvd_ap.some_function()
        self.assertEqual(result, expected_result)

    def test_some_class(self):
        obj = rvd_ap.SomeClass()
        self.assertTrue(obj.some_method())

if __name__ == '__main__':
    unittest.main()
