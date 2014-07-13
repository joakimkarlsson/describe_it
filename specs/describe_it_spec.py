from describe_it import describe, it, before_each

class Fixture(object):
    pass

@describe
def an_outer_context():
    fixture = Fixture()

    @before_each
    def setup():
        fixture.x = 0

    @it
    def it_uses_the_value_initialized_in_before_each():
        assert fixture.x == 0
        fixture.x = 12

    @it
    def it_doesnt_let_tests_interfere_with_each_other():
        assert fixture.x == 0
        fixture.x = 13

    @describe
    def an_inner_context():

        @it
        def it_picks_up_the_outer_contexts_setup():
            assert fixture.x == 0

    @describe
    def augments_fixture():

        @before_each
        def setup():
            fixture.x = 22

        @it
        def gets_augmented_fixture():
            assert fixture.x == 22

        @describe
        def even_more_augmented():

            @before_each
            def setup():
                fixture.x += 10

            @it
            def gets_the_augmented_fixture():
                assert fixture.x == 32
