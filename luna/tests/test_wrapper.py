import unittest
from luna import wrapper


class TestChain(unittest.TestCase):

    def test_execute_sequence(self):
        class Nonlocal:
            pre_run_list = []
            post_run_list = []

        def build_wrapper_class(name):

            class Wrapper(object):

                def __init__(self, args):
                    self.args = args + ['args_' + name]

                def to_args(self):
                    return self.args

                def pre_run(self):
                    Nonlocal.pre_run_list.append("pre_"+name)

                def post_run(self):
                    Nonlocal.post_run_list.append("post_"+name)

            return Wrapper

        class Wrapper4(object):
            def __init__(self, args):
                pass

        wrapper1 = build_wrapper_class('wrapper1')
        wrapper2 = build_wrapper_class('wrapper2')
        wrapper3 = build_wrapper_class('wrapper3')

        w = wrapper.chain([wrapper1, wrapper2, wrapper3, Wrapper4])([])

        w.pre_run()
        w.post_run()

        self.assertEqual(['pre_wrapper1', 'pre_wrapper2', 'pre_wrapper3'], Nonlocal.pre_run_list)
        self.assertEqual(['post_wrapper3', 'post_wrapper2', 'post_wrapper1'],
                         Nonlocal.post_run_list)
        self.assertEqual(['args_wrapper1', 'args_wrapper2', 'args_wrapper3'], w.to_args())
