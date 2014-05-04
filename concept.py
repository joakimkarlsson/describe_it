#!/usr/bin/env python
import sys
import pprint
import functools

pprint = pprint.PrettyPrinter().pprint


contexts = []
context_stack = []

def current_context():
    return context_stack[-1] if context_stack else None


class Context:
    def __init__(self, function, parent=None):
        self.function = function
        self.parent = parent
        self.specs = []
        self.before_eaches = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Context({0}, {1})'.format(repr(self.function.__name__),
                                          repr(self.parent))
    
    def add_spec(self, spec):
        self.specs.append(spec)

    def add_before_each(self, before_each):
        self.before_eaches.append(before_each)

    def run(self):
        for spec in self.specs:
            self.before_each()
            spec()

    def before_each(self):
        if self.parent:
            self.parent.before_each()

        for be in self.before_eaches:
            be()


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


def before_each(setup):
    context = current_context()
    if not context:
        raise Exception("Adding a 'before_each' without describing something "
                        "seems a bit silly.")

    context.add_before_each(setup)


def run_contexts():
    for c in contexts:
        c.run()

class Fixture():
    pass


@describe
def outermost():

    fix = Fixture()

    @before_each
    def setup():
        fix.a = 2
        fix.b = 23

    @describe
    def innermost():

        @before_each
        def setup():
            fix.b = 2

        @it
        def can_fail():
            assert fix.a == 2
            assert fix.b == 2

    @it
    def check_again():
        pprint(fix.__dict__)


@describe
def another_outermost():

    @describe
    def another_innermost():
        pass


def main():
    pprint(contexts)


    run_contexts()


if __name__ == '__main__':
    sys.exit(main())
