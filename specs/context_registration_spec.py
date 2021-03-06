import describe_it as di
from nose.tools import (assert_is_instance, assert_equal,
                        assert_is_none, assert_false, assert_true)


def empty_describe_fn():
    pass


@di.describe
def context_registration():
    fixture = di.Fixture()

    @di.before_each
    def setup():
        fixture.registered_contexts = []
        fixture.active_contexts = []

    def describe(describe_fn):
        di.describe(describe_fn=describe_fn,
                    registered_contexts=fixture.registered_contexts,
                    active_contexts=fixture.active_contexts)

    def xdescribe(describe_fn):
        di.xdescribe(describe_fn=describe_fn,
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

        @di.it
        def is_not_marked_as_skipped_by_default():
            describe(empty_describe_fn)
            top_level = fixture.registered_contexts[0]
            assert_false(top_level.skip)

        @di.it
        def can_be_marked_as_skipped():
            xdescribe(empty_describe_fn)
            top_level = fixture.registered_contexts[0]
            assert_true(top_level.skip)

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
            subs = list(filter(lambda c: c.parent == fixture.top_level,
                          fixture.registered_contexts))
            assert_equal(len(subs), 1)

