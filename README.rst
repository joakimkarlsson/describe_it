describe it
===========

|buildstatus|_

Installing
----------
.. code:: bash

    $ pip install describe-it

Writing
-------
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

        @after_each
        def teardown():
            # This should rarely be needed!
            perform_post_test_cleanup_if_needed()

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

Running
-------
.. code:: bash

    $ nosetests --with-describe-it

.. |buildstatus| image:: https://travis-ci.org/joakimkarlsson/describe_it.svg
.. _buildstatus: https://travis-ci.org/joakimkarlsson/describe_it
