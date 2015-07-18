import describe_it as di
from nose.tools import assert_equal


def empty_describe_fn():
    pass


def empty_it_fn():
    pass


def empty_before_each_fn():
    pass


def empty_after_each_fn():
    pass


@di.describe
def method_registration():
    f = di.Fixture()

    @di.before_each
    def setup():
        f.registered_contexts = []
        f.active_contexts = []
        f.registered_it_fns = []
        f.top_level = di.Context(describe_fn=empty_describe_fn,
                                       parent=None)
        f.registered_contexts.append(f.top_level)
        f.active_contexts.append(f.top_level)

    @di.it
    def starts_without_any_registered_it_functions():
        assert_equal(len(f.registered_it_fns), 0)

    @di.it
    def starts_without_any_registered_before_each_functions():
        assert_equal(len(f.top_level.before_each_fns), 0)

    @di.it
    def starts_without_any_registered_after_each_functions():
        assert_equal(len(f.top_level.after_each_fns), 0)

    @di.it
    def can_register_an_it_method():
        di.it(it_fn=empty_it_fn,
              registered_it_fns=f.registered_it_fns,
              active_contexts=f.active_contexts)

        assert_equal(f.registered_it_fns[0], empty_it_fn)

    @di.it
    def the_registered_it_method_has_the_correct_context():
        di.it(it_fn=empty_it_fn,
              registered_it_fns=f.registered_it_fns,
              active_contexts=f.active_contexts)

        assert_equal(f.registered_it_fns[0].context, f.top_level)

    @di.it
    def the_registered_it_method_is_not_marked_as_skip():
        di.it(it_fn=empty_it_fn,
              registered_it_fns=f.registered_it_fns,
              active_contexts=f.active_contexts)

        assert_equal(f.registered_it_fns[0].should_skip(), False)

    @di.it
    def can_register_a_method_as_skipped():
        di.xit(it_fn=empty_it_fn,
               registered_it_fns=f.registered_it_fns,
               active_contexts=f.active_contexts)

        assert_equal(f.registered_it_fns[0].should_skip(), True)

    @di.it
    def can_register_a_before_each_function():
        di.before_each(before_each_fn=empty_before_each_fn,
                       registered_contexts=f.registered_contexts,
                       active_contexts=f.active_contexts)

        assert_equal(f.top_level.before_each_fns[0], empty_before_each_fn)

    @di.it
    def can_register_a_after_each_function():
        di.after_each(after_each_fn=empty_after_each_fn,
                      registered_contexts=f.registered_contexts,
                      active_contexts=f.active_contexts)

        assert_equal(f.top_level.after_each_fns[0], empty_after_each_fn)

    @di.it
    def can_register_a_method_with_data():
        def can_add(term1,  term2, expected):
            assert (term1 + term2) == expected

        decorator = di.with_data([(1, 1, 2)])
        decorator(can_add,
                  registered_it_fns=f.registered_it_fns,
                  active_contexts=f.active_contexts)

        assert_equal(f.registered_it_fns[0].__name__, 'can_add_1')

    @di.with_data([(1, 2, 3),
                   (3, 4, 7)])
    def can_add(t1, t2, expected):
        assert_equal(t1+t2, expected)
