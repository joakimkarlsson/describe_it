#!/usr/bin/env python
import sys
import pprint

contexts = []
context_stack = []


class Context:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Context({0}, {1})'.format(repr(self.name), repr(self.parent))

def describe(name):
    def decorator(fn):
        print('Registering context {0}...'.format(name))

        parent = context_stack[-1] if len(context_stack) else None
        context = Context(name, parent)

        contexts.append(context)
        context_stack.append(context)
        fn()
        context_stack.pop()

    return decorator

@describe('outermost')
def _():
    print('Inside outermost')

    @describe('innermost')
    def _():
        print('Inside innermost')


@describe('another outermost')
def _():

    @describe('another innermost')
    def _():
        pass


def main():
    pp = pprint.PrettyPrinter()
    pp.pprint(contexts)


if __name__ == '__main__':
    sys.exit(main())
