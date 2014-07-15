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
    def with_a_before_each_function():

        @before_each
        def setup():
            f.before_each = MagicMock()
            f.context.add_before_each(f.before_each)

        @it
        def calls_before_each_before_it_calls_the_it_function():
            def it_fn():
                f.before_each.assert_called_once_with()

            f.context.run_it(it_fn)

        @describe
        def with_a_child_context():

            @before_each
            def setup():
                f.child_context = Context(describe_fn=empty_describe_fn,
                                          parent=f.context)

            @it
            def calls_before_each_on_parent_before_running_it_function():
                def it_fn():
                    f.before_each.assert_called_once_with()

                f.child_context.run_it(it_fn)
