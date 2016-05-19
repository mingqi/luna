'''
Created on 2016-03-21

@author: sincera
'''
import settings


class Run(object):
    def __init__(self, args):
        self.app_id = None
        self.instance_id = None
        self.container_name = None
        self.args = args
        for i in range(len(args)):
            if args[i] == '-e' and args[i+1].startswith('MESOS_TASK_ID='):
                values = args[i+1][len('MESOS_TASK_ID='):].replace('-', '_').split('.')
                self.app_id, self.instance_id = values[0], values[1]
            elif args[i] == '--name':
                self.container_name = args[i+1]

    def to_args(self):
        if settings.DOCKER_LOG_SETTINGS['driver'] == 'fluentd':
            log_args = []
            log_args.append('--log-driver=fluentd')
            log_args.append('--log-opt')
            log_args.append('fluentd-address={}'.format(settings.DOCKER_LOG_SETTINGS['host']))
            log_args.append('--log-opt')
            log_args.append('fluentd-tag=docker.{}.{}.{}'.format(self.app_id, self.instance_id,
                                                                 self.container_name))
            log_args.extend(self.args)
            return log_args
        return self.args
