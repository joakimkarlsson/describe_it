import unittest
import describe_it as di
from expect_it import expect

def empty_describe_fn():
    pass

class TestContextRegistration(unittest.TestCase):

    def setUp(self):
        self.registered_contexts = []
        self.active_contexts = []

    def test_register_one_top_level_context(self):
        self.describe(empty_describe_fn)

        expect(self.registered_contexts[0]).to.be.instance_of(di.Context)
        expect(self.registered_contexts[0].describe_fn).to.equal(
            empty_describe_fn)
        expect(self.registered_contexts[0].parent).to.equal(None)

    def describe(self, describe_fn):
        di.describe(describe_fn=describe_fn,
                    registered_contexts=self.registered_contexts,
                    active_contexts=self.active_contexts)
