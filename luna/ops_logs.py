'''
Created on 2016-03-21

@author: sincera
'''
from luna import docker_cli_parser
from luna import util
import settings

class Pull(object):
    def __init__(self, args):
        opts, args = docker_cli_parser.run(args)
        self.app_id = None
        self.instance_id = None
        self.args = args
        for env in opts.get('env', []):
            name, value = env.split('=', 1)
            if name == 'MESOS_TASK_ID':
                values = value.replace('-', '_').split('.')
                self.app_id, self.instance_id = values[0], values[1]
                break
        self.container_name = opts.get('name')

    def pre_run(self):
        if self.app_id and self.instance_id:
            util.flush_ops_logs(settings.DOCKER_OPS_LOGS_FILE,
                                self.app_id,
                                self.instance_id,
                                self.container_name,
                                'Start pulling {}'.format(self.args[0]),
                                'stdout')
