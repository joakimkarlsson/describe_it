class Grammar(object):

    def __init__(self, actual):
        self.actual = actual

    @property
    def to(self):
        return self

    @property
    def be(self):
        return self

    def instance_of(self, expected_type):
        assert isinstance(self.actual, expected_type)

    def equal(self, expected):
        assert self.actual == expected

def expect(actual):
    return Grammar(actual)
