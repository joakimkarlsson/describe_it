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

    @it
    def doesnt_call_it_fn_if_marked_as_skip():
        try:
            f.it_fn.skip = True
            f.testcase.run_test()
        except SkipTest:    # Letting this bubble up would mark this test as
                            # skipped.
            pass

        assert not f.it_fn.called

    @it
    def throws_SkipTest_if_marked_as_skip():
        f.it_fn.skip = True
        assert_raises(SkipTest, f.testcase.run_test)
