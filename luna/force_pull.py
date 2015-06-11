from luna import docker_cli_parser
import subprocess
import sys


class Run(object):
    def __init__(self, args):
        opts, args = docker_cli_parser.run(args)
        self.image = args[0]

    def pre_run(self):
        print "to force pull docker image before run {}".format(self.image)
        subprocess.check_output(('docker pull '+self.image).split(),
                              stderr=sys.stderr)
