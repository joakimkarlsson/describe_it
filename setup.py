#!/usr/bin/env python
from setuptools import setup

setup(
    name='describe_it',
    version='2.1.0',
    description=('A nose plugin that supports writing describe/it style '
                 'unit tests with nested contexts'),
    long_description=open('README.rst').read(),
    license=open('LICENSE.txt').read(),
    url='https://github.com/joakimkarlsson/describe_it',
    author='Joakim Karlsson',
    author_email='joakim@jkarlsson.com',

    packages=['describe_it'],
    include_package_data = True,
    install_requires=['nose>=1.3.3'],

    tests_require=['nose>=1.3.3', 'mock>=1.0.1'],
    test_suite='nose.collector',

    entry_points={
        'nose.plugins.0.10': [
            'describe_it=describe_it.noseplugin:DescribeItPlugin'
        ]
    },

    keywords=['unit testing', 'tdd', 'bdd', 'nose']
)
