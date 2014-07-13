#!/usr/bin/env python
from setuptools import setup

setup(
    name = 'describe_it',
    description = 'unit testing with describe/it syntax and nested contexts',
    version = '0.1.0',
    author = 'Joakim Karlsson',
    author_email = 'joakim@jkarlsson.com',
    packages = ['describe_it'],

    test_suite = 'tests.test_all',

    entry_points = {
        'nose.plugins.0.10': [
            'describe_it = describe_it.noseplugin:DescribeItPlugin'
        ]
    }
)
