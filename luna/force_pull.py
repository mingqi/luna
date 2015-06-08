from luna import util
import subprocess
import sys


class Run(object):
    def __init__(self, args):
        args = util.parse_run_cli(args)
        self.image = args['IMAGE']

    def pre_run(self):
        print "to force pull docker image before run {}".format(self.image)
        subprocess.check_call(('docker pull '+self.image).split(),
                              stdout=sys.stdout, stderr=sys.stderr)
