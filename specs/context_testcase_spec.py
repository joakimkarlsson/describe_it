from describe_it import describe, it, before_each, Fixture, Context
from describe_it.noseplugin import ContextTestCase
from mock import MagicMock
from nose.tools import assert_raises
from unittest import SkipTest


@describe
def context_testcase():
    f = Fixture()

    @before_each
    def setup():
        f.describe_fn = MagicMock()
        f.context = Context(describe_fn=f.describe_fn, parent=None)
        f.it_fn = MagicMock()
        f.it_fn.skip = False
        f.it_fn.context = f.context
        f.testcase = ContextTestCase(it_fn=f.it_fn)

    @it
    def calls_it_fn():
        f.testcase.run_test()
        f.it_fn.assert_called_once_with()

    @describe
    def context_marked_as_skipped():

        @before_each
        def setup():
            f.context.skip = True

        @it
        def doesnt_call_it_fn():
            try:
                f.testcase.run_test()
            except SkipTest:    # Letting this bubble up would mark this test as
                                # skipped.
                pass

            assert not f.it_fn.called

        @it
        def throws_SkipTest():
            assert_raises(SkipTest, f.testcase.run_test)

    @describe
    def it_fn_marked_as_skipped():

        @before_each
        def setup():
            f.it_fn.skip = True

        @it
        def doesnt_call_it_fn():
            try:
                f.testcase.run_test()
            except SkipTest:    # Letting this bubble up would mark this test as
                                # skipped.
                pass

            assert not f.it_fn.called

        @it
        def throws_SkipTest():
            assert_raises(SkipTest, f.testcase.run_test)

    @describe
    def context_has_a_parent():

        @before_each
        def setup():
            f.child_context = Context(describe_fn=f.describe_fn,
                                      parent=f.context)
            f.it_fn.context = f.child_context

        @it
        def calls_it_fn():
            f.testcase.run_test()
            f.it_fn.assert_called_once_with()

        @describe
        def parent_is_marked_as_skipped():

            @before_each
            def setup():
                f.context.skip = True

            @it
            def doesnt_call_it_fn():
                try:
                    f.testcase.run_test()
                except SkipTest:    # Letting this bubble up would mark this
                                    # test as skipped.
                    pass

                assert not f.it_fn.called
