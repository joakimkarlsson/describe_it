from describe_it import describe, it, before_each, Fixture, Context
from mock import MagicMock


def empty_describe_fn():
    pass


@describe
def context():
    f = Fixture()

    @before_each
    def setup():
        f.context = Context(describe_fn=empty_describe_fn,
                            parent=None)

    @it
    def calls_an_it_function():
        it_fn = MagicMock()
        f.context.run_it(it_fn)
        it_fn.assert_called_once_with()

    @describe
    def with_before_each_and_after_each_functions():

        @before_each
        def setup():
            f.before_each = MagicMock()
            f.after_each = MagicMock()
            f.context.add_before_each(f.before_each)
            f.context.add_after_each(f.after_each)

        @it
        def calls_before_each_when_asked():
            f.context.run_before_eaches()
            f.before_each.assert_called_once_with()

        @it
        def calls_after_each():
            f.context.run_after_eaches()
            f.after_each.assert_called_once_with()

        @describe
        def with_a_child_context():

            @before_each
            def setup():
                f.child_context = Context(describe_fn=empty_describe_fn,
                                          parent=f.context)

            @it
            def calls_before_each_on_parent_before_running_its_own():
                def child_before_each():
                    f.before_each.assert_called_once_with()

                f.child_context.add_before_each(child_before_each)
                f.child_context.run_before_eaches()

            @it
            def calls_after_each_on_parent_after_running_its_own():

                def child_after_each():
                    assert not f.after_each.called

                f.child_context.add_after_each(child_after_each)
                f.child_context.run_after_eaches()
