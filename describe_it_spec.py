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
    def should_do_something():
        assert fixture.x == 0
        fixture.x = 12

    @it
    def should_do_something_else():
        assert fixture.x == 0
        fixture.x = 13

    @describe
    def an_inner_context():

        @it
        def should_do_something():
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
            def should_work():
                assert fixture.x == 32
