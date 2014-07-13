import unittest
from specs.contexts import TestContextRegistration
import describe_it_spec
from describe_it.noseplugin import DescribeItPlugin


def test_all():
    suite = unittest.TestSuite()

    loader = unittest.TestLoader()
    suite.addTest(loader.loadTestsFromTestCase(TestContextRegistration))

    plugin = DescribeItPlugin()
    testcases = plugin.loadTestsFromModule(describe_it_spec)
    for tc in testcases:
        suite.addTest(tc)

    return suite
