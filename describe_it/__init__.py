import sys

registered_contexts = []
active_contexts = []

def get_contexts_for_module(module):
    return (c for c in registered_contexts if c.module == module)

class Context(object):

    def __init__(self, describe_fn, parent):
        self.describe_fn = describe_fn
        self.parent = parent
        self.it_fns = []

    @property
    def module(self):
        return sys.modules[self.describe_fn.__module__]

    def add_it_fn(self, it_fn):
        self.it_fns.append(it_fn)


def describe(describe_fn,
             registered_contexts=registered_contexts, 
             active_contexts=active_contexts):

    parent = _current_active_context()

    context = Context(describe_fn=describe_fn,parent=parent)

    registered_contexts.append(context)

    active_contexts.append(context)
    describe_fn()
    active_contexts.pop()


def it(it_fn,
       registered_contexts=registered_contexts,
       active_contexts=active_contexts):

    context = _current_active_context()
    if not context:
        raise Exception("Adding an 'it' without telling me what you're "
                        "describing seems a bit silly.")

    context.add_it_fn(it_fn)

def _current_active_context():
    return active_contexts[-1] if active_contexts else None
