import describe_it as di
from nose.tools import assert_equal

def empty_describe_fn():
    pass

def empty_it_fn():
    pass

def empty_before_each_fn():
    pass

@di.describe
def method_registration():
    f = di.Fixture()

    @di.before_each
    def setup():
        f.registered_contexts = []
        f.active_contexts = []
        f.top_level = di.Context(describe_fn=empty_describe_fn,
                                       parent=None)
        f.registered_contexts.append(f.top_level)
        f.active_contexts.append(f.top_level)

    @di.it
    def starts_without_any_registered_it_functions():
        assert_equal(len(f.top_level.it_fns), 0)

    @di.it
    def starts_without_any_registered_before_each_functions():
        assert_equal(len(f.top_level.before_each_fns), 0)

    @di.it
    def can_register_an_it_method():
        di.it(it_fn=empty_it_fn,
              registered_contexts=f.registered_contexts,
              active_contexts=f.active_contexts)

        assert_equal(f.top_level.it_fns[0], empty_it_fn)

    @di.it
    def can_register_a_before_each_function():
        di.before_each(before_each_fn=empty_before_each_fn,
                       registered_contexts=f.registered_contexts,
                       active_contexts=f.active_contexts)

        assert_equal(f.top_level.before_each_fns[0], empty_before_each_fn)
