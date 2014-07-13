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
            test_cases = (create_testcases_for_context(c)
                          for c in di.get_contexts_for_module(module))
            return itertools.chain(*test_cases)


class ContextTestCase(unittest.TestCase):

    def __init__(self, context, it_fn):
        self.context = context
        self.it_fn = it_fn
        unittest.TestCase.__init__(self, methodName='run_test')

    def run_test(self):
        self.context.run_before_eaches()
        self.it_fn()

    def __str__(self):
        return '{0}: {1}'.format(str(self.context), self.it_fn.__name__)


def create_testcases_for_context(context):
    def create_it(it_fn):
        return ContextTestCase(context, it_fn)
    return map(create_it, context.it_fns)


if __name__ == "__main__":
    log.setLevel(logging.DEBUG)
    nose.main(addplugins=[DescribeItPlugin()])
