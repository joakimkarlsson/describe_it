#!/usr/bin/env python
from setuptools import setup

setup(
    name='describe_it',
    description='unit testing with describe/it syntax and nested contexts',
    url='https://github.com/joakimkarlsson/describe_it',
    version='0.1.0',
    author='Joakim Karlsson',
    author_email='joakim@jkarlsson.com',
    packages=['describe_it'],

    tests_require=['nose>=1.3.3'],
    test_suite='nose.collector',

    entry_points={
        'nose.plugins.0.10': [
            'describe_it=describe_it.noseplugin:DescribeItPlugin'
        ]
    }
)
