registered_contexts = []
active_contexts = []

class Context(object):

    def __init__(self, describe_fn, parent):
        self.describe_fn = describe_fn
        self.parent = parent


def describe(describe_fn,
             registered_contexts=registered_contexts, 
             active_contexts=active_contexts):
    registered_contexts.append(Context(describe_fn=describe_fn, parent=None))
