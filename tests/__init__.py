import unittest
from tests.contexts import TestContextRegistration

def test_all():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    suite.addTest(loader.loadTestsFromTestCase(TestContextRegistration))
    return suite
