describe it
===========

A nose plugin for describe/it syntax

Installing it::

    pip install describe-it

Writing a test::

    >vim myfirst_spec.py

    from game import Game
    from describe_it import describe, it, before_each, Fixture

    @describe
    def a_game():
        f = Fixture()

        @before_each
        def setup():
            f.game = Game()

        @it
        def is_player_ones_turn():
            assert f.game.current_player == 1

        @describe
        def in_second_round():

            @before_each
            def setup():
                f.game.play_round()

            @it
            def is_player_twos_turn():
                assert f.game.current_player == 2

Running tests::

    nosetests --with-describe-it

At the moment only files ending with 'spec.py' are considered to contain tests for describe/it (this will probably change).
