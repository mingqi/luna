import random
import settings
import socket
import requests
import iptables
import json
import uuid
import traceback
from functools import partial
from docker import Client as DockerClient


def random_mac():
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


def service_detail(namespace, name, application=None):
    if application:
        url = '%s/v1/services/%s/%s?application=%s' % \
            (settings.JAKIRO['API_ENDPOINT'], namespace, name, application)
    else:
        url = '%s/v1/services/%s/%s' % (settings.JAKIRO['API_ENDPOINT'],
                                        namespace, name)
    r = requests.get(url, auth=(settings.JAKIRO['USER'],
                                settings.JAKIRO['PASSWORD']))

    if r.status_code >= 400 and r.status_code < 500:
        return None

    if r.status_code >= 500:
        raise RESTCallException(r.status_code, r.text)

    return r.json()


def get_ip(domain_name):
    return socket.gethostbyname(domain_name)


def add_link_rule(protocol, ip, port, mac_address):
    """
    add iptable rule to open traffic of linked service
    protocol, ip and port is linked service endpoint
    mac_address is linking service instance's mac address
    """
    chain = iptables.get_chain('filter', settings.IPTABLE_CHAIN_NAME)
    if not chain:
        chain = iptables.create_chain('filter', settings.IPTABLE_CHAIN_NAME)
    rule = iptables.rule(dst='{}/32'.format(ip),
                         in_interface='docker0',
                         protocol=protocol,
                         match={
                            'mac': {
                                'mac-source': mac_address
                            },
                            protocol: {
                                'dport': str(port)
                            }
                         },
                         target='ACCEPT')
    chain.append_rule(rule)


def conv_rule(rule):
    """
    convert iptables rule to a concise tuple: (protocol, ip, port, mad_address)
    """
    rule.protocol
    mac_match = next((m for m in rule.matches if m.name == 'mac'), None)
    proto_match = next((m for m in rule.matches if m.name == rule.protocol), None)

    if not mac_match:
        raise Exception('not found mac match in rule')
    if not proto_match:
        raise Exception('not found %s match in rule' % rule.protocol)

    return (rule.protocol, rule.dst.split('/')[0],
            int(proto_match.dport), mac_match.mac_source)


def link_rules_for_service(service_uuid, mac_address):
    rules = []
    configs = service_configs(service_uuid)
    if not configs:
        raise Exception('service {} is not exists'.format(service_uuid))
    namespace = configs['namespace']
    application = configs.get('application')
    for linked_to_app_name in json.loads(configs['linked_to_apps']).keys():
        detail = service_detail(namespace, linked_to_app_name, application)
        if not detail:
            continue
        for p in detail['instance_ports']:
            endpoint_type = p.get('endpoint_type', None)
            if not endpoint_type:
                continue
            if endpoint_type == 'internal-endpoint':
                rules.append((p['protocol'],
                              get_ip(p['default_domain']),
                              p['service_port'],
                              mac_address))
    return rules


def is_uuid(id):
    try:
        uuid.UUID(id)
        return True
    except ValueError:
        return False


class Run(object):
    """
    wrap for docker run command.
    to setup firewall to allow traffic for linked apps
    """

    def __init__(self, args):
        self.args = args
        self.mac_address = random_mac()
        service_uuid = None
        for i in range(len(args)):
            if args[i] == '-e' and args[i+1].startswith('MARATHON_APP_ID='):
                service_uuid = args[i+1][len('MARATHON_APP_ID=')+1:]

        if service_uuid and is_uuid(service_uuid):
            self.rules = link_rules_for_service(service_uuid, self.mac_address)
        else:
            self.rules = []

    def pre_run(self):
        for rule in self.rules:
            add_link_rule(*rule)

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
