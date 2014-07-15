import sys

registered_contexts = []
active_contexts = []


class Fixture(object):
    pass


def get_contexts_for_module(module):
    return (c for c in registered_contexts if c.module == module)


class Context(object):

    def __init__(self, describe_fn, parent):
        self.describe_fn = describe_fn
        self.parent = parent
        self.it_fns = []
        self.before_each_fns = []

    @property
    def module(self):
        return sys.modules[self.describe_fn.__module__]

    def add_it_fn(self, it_fn):
        self.it_fns.append(it_fn)

    def add_before_each(self, before_each_fn):
        self.before_each_fns.append(before_each_fn)

    def run_before_eaches(self):
        if self.parent:
            self.parent.run_before_eaches()

        for be in self.before_each_fns:
            be()

    def run_it(self, it_fn):
        self.run_before_eaches()
        it_fn()

    def __str__(self):
        if self.parent:
            return '{0} {1}'.format(
                str(self.parent), self.describe_fn.__name__)
        return self.describe_fn.__name__


def describe(describe_fn,
             registered_contexts=registered_contexts,
             active_contexts=active_contexts):

    parent = _current_active_context(active_contexts=active_contexts)

    context = Context(describe_fn=describe_fn, parent=parent)

    registered_contexts.append(context)

    active_contexts.append(context)
    describe_fn()
    active_contexts.pop()


def it(it_fn,
       registered_contexts=registered_contexts,
       active_contexts=active_contexts):

    context = _current_active_context(active_contexts=active_contexts)
    if not context:
        raise Exception("Adding an 'it' without telling me what you're "
                        "describing seems a bit silly.")

    context.add_it_fn(it_fn)


def before_each(before_each_fn,
                registered_contexts=registered_contexts,
                active_contexts=active_contexts):

    context = _current_active_context(active_contexts=active_contexts)
    if not context:
        raise Exception("Adding a 'before_each' without describing something "
                        "seems a bit silly.")

    context.add_before_each(before_each_fn)


def _current_active_context(active_contexts=active_contexts):
    return active_contexts[-1] if active_contexts else None
