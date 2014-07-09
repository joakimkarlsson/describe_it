#!/usr/bin/env python
import logging
from nose.plugins import Plugin
import nose
import re

log = logging.getLogger('nose.plugins.describe_it')

class DescribeItPlugin(Plugin):
    name = 'describe-it'

    def wantFile(self, file):
        is_spec_file = re.search('spec\.py$', file)
        log.debug(
            'wantFile: {0} - {1}'.format(file, 
                                         'yes' if is_spec_file else 'no'))
        return is_spec_file


if __name__ == "__main__":
    log.setLevel(logging.DEBUG)
    nose.main(addplugins=[DescribeItPlugin()])
