import settings


class Run(object):
    """
    append --dns options to docker run
    """
    def __init__(self, args):
        self.args = args

    def to_args(self):
        for dns in reversed(settings.DNS):
            self.args.insert(0, dns)
            self.args.insert(0, '--dns')
        return self.args
