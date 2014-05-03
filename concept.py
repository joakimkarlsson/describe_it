#!/usr/bin/env python
import sys
import pprint

contexts = []
context_stack = []


def describe(name):
    def decorator(context):
        print('Registering context {0}...'.format(name))
        my_parent = context_stack[-1] if len(context_stack) else None
        contexts.append((name, context, my_parent))
        context_stack.append(context)
        context()
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
