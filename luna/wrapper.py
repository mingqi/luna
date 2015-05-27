import random
import settings
import socket
import requests
import iptables
import json
import traceback
from functools import partial
from docker import Client as DockerClient


def randomMAC():
    mac = [0x02, 0x42, 0xac, 0x11,
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]

    return ':'.join(map(lambda x: "%02x" % x, mac))


class RESTCallException(Exception):

    def __init__(self, status_code, message):
        super(Exception, self).__init__()
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return repr('code: %d, message: %s' % (self.status_code, self.message))

def service_configs(uuid):
    r = requests.get('%s/v1/appconfigs/%s' %
                     (settings.JAKIRO['INNER_API_ENDPOINT'], uuid),
                     auth=(settings.JAKIRO['USER'],
                           settings.JAKIRO['PASSWORD']))

    if r.status_code >= 400 and r.status_code < 500:
        return None

    if r.status_code >= 500:
        raise RESTCallException(r.status_code, r.text)

    return r.json()


def service_detail(namespace, name):
    r = requests.get('%s/v1/services/%s/%s' %
                     (settings.JAKIRO['API_ENDPOINT'], namespace, name),
                     auth=(settings.JAKIRO['USER'],
                           settings.JAKIRO['PASSWORD']))

    if r.status_code >= 400 and r.status_code < 500:
        return None

    if r.status_code >= 500:
        raise RESTCallException(r.status_code, r.text)

    return r.json()


def getIP(domain_name):
    return socket.gethostbyname(domain_name)


def add_allow_rule(ip, port, mac_address):
    chain = iptables.get_chain('filter', settings.IPTABLE_CHAIN_NAME)
    if not chain:
        chain = iptables.create_chain('filter', settings.IPTABLE_CHAIN_NAME)
    rule = iptables.rule(dst='{}/32'.format(ip),
                         in_interface='docker0',
                         match={
                            'mac': {
                                'mac-source': mac_address
                            }
                         },
                         target='ACCEPT')
    chain.append_rule(rule)


class Run(object):
    """
    wrap for docker run command.
    to setup firewall to allow traffic for linked apps 
    """

    def __init__(self, args):
        self.args = args
        self.mac_address = randomMAC()
        self.allowed = []
        service_uuid = None
        for i in range(len(args)):
            if args[i] == '-e' and args[i+1].startswith('MARATHON_APP_ID='):
                service_uuid = args[i+1][len('MARATHON_APP_ID=')+1:]

        if not service_uuid:
            raise Exception('not found MARATHON_APP_ID environment')

        configs = service_configs(service_uuid)
        if not configs:
            raise Exception('service {} is not exists'.format(service_uuid))
        namespace = configs['namespace']
        for linked_to_app_name in json.loads(configs['linked_to_apps']).keys():
            detail = service_detail(namespace, linked_to_app_name)
            service_ip = getIP(detail['default_domain_name'])
            for instance_port in detail['instance_ports']:
                service_port = instance_port['service_port']
        self.allowed.append((service_ip, service_port))

    def pre_run(self):
        for ip, port in self.allowed:
            add_allow_rule(ip, port, self.mac_address)

    def to_args(self):
        return ['--mac-address=%s' % self.mac_address] + self.args


class Wait(object):
    """
    wrap docker wait. Cleanup firewall rules after containers exit
    """

    def __init__(self, args):
        docker = DockerClient(base_url='unix://var/run/docker.sock',
                              version=settings.DOCKER_API_VERSION)
        self.mac_address_list = []
        for container in args:
            try:
                container_info = docker.inspect_container(container)
                if not container_info['State']['Running']:
                    continue
                self.mac_address_list.append(
                    container_info['NetworkSettings']['MacAddress'].upper())
            except Exception:
                traceback.print_exc()

    def post_run(self):
        chain = iptables.get_chain('filter', settings.IPTABLE_CHAIN_NAME)
        if not chain:
            return

        map(chain.delete_rule,
            filter(partial(iptables.is_rule_of_mac_source,
                           mac_source_list=self.mac_address_list),
                   chain.rules))
