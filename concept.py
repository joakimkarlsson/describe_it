#!/usr/bin/env python
import sys
import pprint

contexts = []
context_stack = []

def current_context():
    return context_stack[-1] if context_stack else None


class Context:
    def __init__(self, function, parent=None):
        self.function = function
        self.parent = parent
        self.specs = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Context({0}, {1})'.format(repr(self.function.__name__),
                                          repr(self.parent))
    
    def add_spec(self, spec):
        self.specs.append(spec)

def describe(context_fn):
    parent = current_context()
    context = Context(context_fn, parent)

    contexts.append(context)
    context_stack.append(context)
    context_fn()
    context_stack.pop()


def it(spec):
    context = current_context()
    if not context:
        raise Exception("Adding an 'it' without telling me what you're "
                        "describing seems a bit silly.")

    context.add_spec(spec)


@describe
def outermost():

    @describe
    def innermost():

        @it
        def can_fail():
            assert 1 == 0


@describe
def another_outermost():

    @describe
    def another_innermost():
        pass


def main():
    pp = pprint.PrettyPrinter()
    pp.pprint(contexts)


if __name__ == '__main__':
    sys.exit(main())
