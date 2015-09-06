from luna import docker_cli_parser


class Run(object):

    def __init__(self, args):
        self.args = args
        opts, args = docker_cli_parser.run(args)
        self.mem_oversell_rate = 1
        for env in opts.get('env', []):
            name, value = env.split('=')
            if name == '__ALAUDA_OVER_COMMIT_MEM_RATE__':
                self.mem_oversell_rate = float(value)
        self.memory = int(opts.get('memory', None))

    def to_args(self):
        if self.memory:
            self.memory = int(self.memory * self.mem_oversell_rate)
            self.args[self.args.index('-m') + 1] = str(self.memory)
        return self.args
