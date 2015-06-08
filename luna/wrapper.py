import functools


def give_default_methods(Wrapper):
    class DefaultMethods(object):
        def __init__(self, args):
            self.args = args
            self.wrapper = Wrapper(args)

        def to_args(self):
            if not hasattr(self.wrapper, 'to_args'):
                return self.args
            else:
                return self.wrapper.to_args()

        def pre_run(self):
            if hasattr(self.wrapper, 'pre_run'):
                self.wrapper.pre_run()

        def post_run(self):
            if hasattr(self.wrapper, 'post_run'):
                self.wrapper.post_run()

    return DefaultMethods


def chain(Wrappers):

    Wrappers = map(give_default_methods, Wrappers)

    class WrapWrapper(object):
        def __init__(self, Wrappers, args):
            self.wrappers = []
            for Wrapper in Wrappers:
                wrapper = Wrapper(args)
                self.wrappers.append(wrapper)
                args = wrapper.to_args()

            self.args = args

        def to_args(self):
            return self.args

        def pre_run(self):
            for wrapper in self.wrappers:
                wrapper.pre_run()

        def post_run(self):
            for wrapper in reversed(self.wrappers):
                wrapper.post_run()

    return functools.partial(WrapWrapper, Wrappers)

