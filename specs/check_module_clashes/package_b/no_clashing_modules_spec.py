from describe_it import describe, it
from nose.tools import assert_equal
times_this_gets_run = 1

print("bbb")

@describe
def modules_with_the_same_names_should_not_clash():

    @it
    def should_only_be_run_once():
        global times_this_gets_run
        assert_equal(times_this_gets_run, 1)
        times_this_gets_run += 1

