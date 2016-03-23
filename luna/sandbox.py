'''
Created on 2016-03-21

@author: sincera
'''


from luna import docker_cli_parser

class Run(object):
    def __init__(self, args):
        self.args = args
        key = None
        value = None
        for i in range(len(args) - 1):
            if args[i] == '-e' and args[i+1].startswith('MESOS_SANDBOX='):
                key = i
                value = i+1
                break
        if key and value:
            del self.args[value]
            del self.args[key]

    def to_args(self):
        return self.args