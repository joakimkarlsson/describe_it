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

    @describe           # This declares a test context.
    def a_game():
        f = Fixture()   # Fixture is a hack to get around Python's
                        # implementation of closures. You can use
                        # other methods, such as nonlocal if you like.

        @before_each    # Will be called before each 'it' method.
        def setup():
            f.game = Game()

        @after_each     # Will be called after each 'it' method.
        def teardown():
            # This should rarely be needed!
            perform_post_test_cleanup_if_needed()

        @it             # This marks a test method.
        def is_player_ones_turn():
            # describe_it doesn't come with yet another assertion lib.
            # Pick any one you like.
            assert f.game.current_player == 1

        @describe   # This is a nested context that augments the context above.
        def in_second_round():

            # Before each 'it' method, any before_each in outer
            # contexts will be called first. Then this method
            # will be called.
            @before_each
            def setup():
                f.game.play_round()

            @it
            def is_player_twos_turn():
                assert f.game.current_player == 2

     # You can skip whole contexts by using '@xdescribe' or '@describe_skip'
     @xdescribe
     def this_context_is_marked_as_skipped():

        @it
        def this_test_will_be_skipped():
            assert True

     @describe
     def context_with_a_skipped_it_method():

        # You can skip individual test methods by using '@xit' or '@it_skip'
        @xit
        def this_test_will_be_skipped():
            assert True

        @it
        def this_test_will_be_run():
            assert True

Running
-------
.. code:: bash

    $ nosetests --with-describe-it

.. |buildstatus| image:: https://travis-ci.org/joakimkarlsson/describe_it.svg
.. _buildstatus: https://travis-ci.org/joakimkarlsson/describe_it
