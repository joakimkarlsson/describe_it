#!/usr/bin/env python
import logging
import nose
import re
import describe_it as di
import unittest
import itertools

log = logging.getLogger('nose.plugins.describe_it')


class DescribeItPlugin(nose.plugins.Plugin):
    name = 'describe-it'

    def wantModule(self, module):
        return re.search('spec$', module.__name__)

    def wantFile(self, file):
        return re.search('spec\.py$', file)

    def loadTestsFromModule(self, module):
        is_spec_module = re.search('spec$', module.__name__)
        if is_spec_module:
            test_cases = (ContextTestCase(i)
                          for i in di.get_it_fns_for(module))
            return test_cases


class ContextTestCase(unittest.TestCase):

    def __init__(self, it_fn):
        self.it_fn = it_fn
        unittest.TestCase.__init__(self, methodName='run_test')

    def setUp(self):
        self.it_fn.context.run_before_eaches()

    def tearDown(self):
        self.it_fn.context.run_after_eaches()

    def run_test(self):
        self.it_fn()

    def __str__(self):
        return '{0}: {1}'.format(str(self.it_fn.context), self.it_fn.__name__)




if __name__ == "__main__":
    log.setLevel(logging.DEBUG)
    nose.main(addplugins=[DescribeItPlugin()])
