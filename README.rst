describe it
===========

A nose plugin for describe/it syntax

Installing it

.. code:: bash

    $ pip install describe-it

Writing a test
--------------

Any module that ends with 'spec' is considered to contain specifications/tests
for describe_it.

.. code:: bash

    $ vim myfirst_spec.py

...and the content:

.. code:: python
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

Running tests

.. code:: bash

    $ nosetests --with-describe-it
