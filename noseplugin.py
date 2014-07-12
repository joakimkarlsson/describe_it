#!/usr/bin/env python
import logging
from nose.plugins import Plugin
import nose
import re
import describe_it as di
import unittest
import itertools

log = logging.getLogger('nose.plugins.describe_it')

class DescribeItPlugin(Plugin):
    name = 'describe-it'

    def wantModule(self, module):
        is_spec_module = re.search('spec$', module.__name__)
        if is_spec_module:
            log.debug('wantModule({0})'.format(module))
        return is_spec_module

    def wantFile(self, file):
        is_spec_file = re.search('spec\.py$', file)

        if is_spec_file:
            log.debug(
                'wantFile: {0} - {1}'.format(file, 
                                             'yes' if is_spec_file else 'no'))
        return is_spec_file

    def loadTestsFromModule(self, module):
        log.debug('loadTestsFromModule({0})'.format(module))
        is_spec_module = re.search('spec$', module.__name__)
        if is_spec_module:
            test_cases = (create_testcases_for_context(c)
                          for c in di.get_contexts_for_module(module))
            return itertools.chain(*test_cases)


class ContextTestCase(unittest.TestCase):

    def __init__(self, context, it_fn):
        self.context = context
        self.it_fn = it_fn
        unittest.TestCase.__init__(self, methodName='runTest')
        
    def runTest(self):
        self.context.run_before_eaches()
        self.it_fn()


def create_testcases_for_context(context):
    def create_it(it_fn):
        return ContextTestCase(context, it_fn)
    return map(create_it, context.it_fns)


if __name__ == "__main__":
    log.setLevel(logging.DEBUG)
    nose.main(addplugins=[DescribeItPlugin()])
