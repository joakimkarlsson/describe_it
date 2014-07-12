from describe_it import describe, it

@describe
def an_outer_context():

    @it
    def should_do_something():
        assert 1 == 2

    @it
    def should_do_something_else():
        assert 1 == 1

    @describe
    def an_inner_context():

        @it
        def should_do_something():
            assert 1 == 2
