import sys

registered_contexts = []
active_contexts = []
registered_it_fns = []


class Fixture(object):
    pass


def get_it_fns_for(module):
    return (i for i in registered_it_fns if i.context.module == module)


class Context(object):

    def __init__(self, describe_fn, parent, skip=False):
        self.describe_fn = describe_fn
        self.parent = parent
        self.it_fns = []
        self.before_each_fns = []
        self.after_each_fns = []
        self.skip = skip

    @property
    def module(self):
        return sys.modules[self.describe_fn.__module__]

    def add_before_each(self, before_each_fn):
        self.before_each_fns.append(before_each_fn)

    def add_after_each(self, after_each_fn):
        self.after_each_fns.append(after_each_fn)

    def run_before_eaches(self):
        if self.parent:
            self.parent.run_before_eaches()

        for be in self.before_each_fns:
            be()

    def run_after_eaches(self):
        for ae in self.after_each_fns:
            ae()

        if self.parent:
            self.parent.run_after_eaches()

    def should_skip(self):
        return self.skip or self.parent and self.parent.should_skip()

    def __str__(self):
        if self.parent:
            return '{0}, {1}'.format(
                str(self.parent), self.describe_fn.__name__)
        return self.describe_fn.__name__


def describe(describe_fn,
             registered_contexts=registered_contexts,
             active_contexts=active_contexts,
             skip=False):

    parent = _current_active_context(active_contexts=active_contexts)

    context = Context(describe_fn=describe_fn, parent=parent, skip=skip)

    registered_contexts.append(context)

    active_contexts.append(context)
    describe_fn()
    active_contexts.pop()


def xdescribe(describe_fn,
              registered_contexts=registered_contexts,
              active_contexts=active_contexts):
    describe(describe_fn, registered_contexts, active_contexts, skip=True)


def describe_skip(*args, **kwargs):
    xdescribe(*args, **kwargs)


def it(it_fn,
       registered_it_fns=registered_it_fns,
       active_contexts=active_contexts):

    context = _current_active_context(active_contexts=active_contexts)
    if not context:
        raise Exception("Adding an 'it' without telling me what you're "
                        "describing seems a bit silly.")

    it_fn.context = context
    it_fn.skip = False
    registered_it_fns.append(it_fn)


def xit(it_fn,
        registered_it_fns=registered_it_fns,
        active_contexts=active_contexts):

    context = _current_active_context(active_contexts=active_contexts)
    if not context:
        raise Exception("Adding an 'xit' without telling me what you're "
                        "describing seems a bit silly.")

    it_fn.context = context
    it_fn.skip = True
    registered_it_fns.append(it_fn)


def it_skip(*args, **kwargs):
    xit(*args, **kwargs)


def before_each(before_each_fn,
                registered_contexts=registered_contexts,
                active_contexts=active_contexts):

    context = _current_active_context(active_contexts=active_contexts)
    if not context:
        raise Exception("Adding a 'before_each' without describing something "
                        "seems a bit silly.")

    context.add_before_each(before_each_fn)


def after_each(after_each_fn,
               registered_contexts=registered_contexts,
               active_contexts=active_contexts):

    context = _current_active_context(active_contexts=active_contexts)
    if not context:
        raise Exception("Adding a 'after_each' without describing something "
                        "seems a bit silly.")

    context.add_after_each(after_each_fn)


def _current_active_context(active_contexts=active_contexts):
    return active_contexts[-1] if active_contexts else None
