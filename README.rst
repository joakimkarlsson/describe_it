describe it
===========

|buildstatus|_

Describe-it is a nose plugin that allows you to write unit tests that are more
like executable examples of how a component should work than just being tests.

The other benefit is the ability to describe how a component behaves in certain
contexts, where one context may build on a previously defined context by using
nesting.

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

    @describe                                               # This declares a test context.
    def a_game():
        f = Fixture()                                       # Fixture is a hack to get around Python's
                                                            # implementation of closures. You can use
                                                            # other methods, such as nonlocal if you like.

        @before_each                                        # Will be called before each 'it' method.
        def setup():
            f.game = Game()

        @after_each                                         # Will be called after each 'it' method.
        def teardown():
            perform_post_test_cleanup_if_needed()           # This should rarely be needed!

        @it                                                 # This marks a test method.
        def is_player_ones_turn():
            assert f.game.current_player == 1               # describe_it doesn't come with yet another assertion lib.
                                                            # Pick any one you like.

        @describe                                           # This is a nested context that augments the context above.
        def in_second_round():

            @before_each                                    # Before each 'it' method, any before_each in outer
            def setup():                                    # contexts will be called first. Then this method
                f.game.play_round()                         # will be called.

            @it
            def is_player_twos_turn():
                assert f.game.current_player == 2

            @xit                                            # You can skip individual test methods by using '@xit' or '@it_skip'
            def skips_tests():
                assert True

            @with_data([1, 2, 3],                           # You can parameterize tests with different combinations of inputs
                       [3, 4, 9])
            def adds_numbers(term_1, term_2, expected):
                assert (term_1 + term_2) == expected

     @xdescribe                                             # You can skip whole contexts by using '@xdescribe' or '@describe_skip'
     def this_context_is_marked_as_skipped():

        @it
        def this_test_will_be_skipped():
            assert True

Running
-------
.. code:: bash

    $ nosetests --with-describe-it

.. |buildstatus| image:: https://travis-ci.org/joakimkarlsson/describe_it.svg
.. _buildstatus: https://travis-ci.org/joakimkarlsson/describe_it
