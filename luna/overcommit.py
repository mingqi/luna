# from luna import docker_cli_parser


class Run(object):

    def __init__(self, args):
        self.args = args
        self.mem_overcommit_str = ""
        self.cpu_overcommit_str = ""
        for i in range(len(args) - 1):
            if args[i] == '-e' and args[i+1].startswith('__ALAUDA_OVER_COMMIT_MEM__='):
                name, value = args[i+1].split('=')
                self.mem_overcommit_str = filter(str.isdigit, value)
            if args[i] == '-e' and args[i+1].startswith('__ALAUDA_OVER_COMMIT_CPU__='):
                name, value = args[i+1].split('=')
                self.cpu_overcommit_str = value

    def to_args(self):
        if self.mem_overcommit_str:
            pos_m = self.args.index('-m') + 1
            self.args[pos_m] = str(int(float(self.mem_overcommit_str))) + 'M'

        if self.cpu_overcommit_str:
            pos_c = self.args.index('-c') + 1
            self.args[pos_c] = str(int(float(self.cpu_overcommit_str)))

        return self.args
