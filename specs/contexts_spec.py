import unittest
import describe_it as di
from nose.tools import assert_is_instance, assert_equal, assert_is_none

def empty_describe_fn():
    pass

class Fixture(object):
    pass

@di.describe
def context_registration():
    fixture = Fixture()

    @di.before_each
    def setup():
        fixture.registered_contexts = []
        fixture.active_contexts = []

    def describe(describe_fn):
        di.describe(describe_fn=describe_fn,
                    registered_contexts=fixture.registered_contexts,
                    active_contexts=fixture.active_contexts)

    @di.describe
    def a_top_level_context():

        @di.it
        def registers_a_context():
            describe(empty_describe_fn)
            top_level = fixture.registered_contexts[0]
            assert_is_instance(top_level, di.Context)

        @di.it
        def registered_context_wraps_the_function_provided_to_it():
            describe(empty_describe_fn)
            top_level = fixture.registered_contexts[0]
            assert_equal(top_level.describe_fn, empty_describe_fn)

        @di.it
        def has_no_parent():
            describe(empty_describe_fn)
            top_level = fixture.registered_contexts[0]
            assert_is_none(top_level.parent)


    @di.describe
    def a_nested_context():

        @di.before_each
        def setup():
            fixture.top_level = di.Context(describe_fn=empty_describe_fn,
                                           parent=None)
            fixture.registered_contexts.append(fixture.top_level)
            fixture.active_contexts.append(fixture.top_level)

        @di.it
        def registers_a_context():
            describe(empty_describe_fn)
            assert_equal(len(fixture.registered_contexts), 2)

        @di.it
        def has_the_top_level_context_as_parent():
            describe(empty_describe_fn)
            subs = filter(lambda c: c.parent == fixture.top_level,
                          fixture.registered_contexts)
            assert_equal(len(subs), 1)

