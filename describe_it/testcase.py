import unittest

class PyDescribeTestCase(unittest.TestCase):
    def test_fail(self):
        self.assertEqual(1, 0)
