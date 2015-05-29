from os.path import join, abspath
import sys
from pprint import pprint

ROOT_DIR = abspath(join(__file__, '../'))
sys.path.insert(0, ROOT_DIR)

from luna import iptables
from luna import wrapper

# from luna import docker

# chain = iptables.get_chain('filter', 'FOR_TEST')
# rule = iptables.rule(src='192.168.0.1/255.255.255.0', target='ACCEPT')
# chain.append_rule(rule)
# app_config = docker.service_configs('9f29f6b6-b7d9-48e8-a79c-295ab771f609')
# print app_config
# print app_config['namespace']
# print app_config['service_name']

# service = docker.service_detail('vipertest', 'mysql')
# print service['default_domain_name']
# print service['instance_ports']

# print docker.add_allow_rule('1.1.1.2', 3320, '02:42:ac:11:00:00')

# print docker.randomMAC()

# from docker import Client
# c = Client(base_url='unix://var/run/docker.sock')
# print c.containers(quiet=True)

# pprint(c.inspect_container('ppsql')['NetworkSettings']['MacAddress'])
# pprint(c.inspect_container('sad_franklin'))

chain = iptables.get_chain('filter', 'ALAUDA')
rule = chain.rules[0]
print rule.dst.split('/')[0]
print wrapper.conv_rule(rule)
# chain.delete_rule(rule)
# chain.delete_rule(rule)
# for rule in chain.rules:
#     for match in rule.matches:
#         print match.parameters

# def ff(name, title):
#     print "name:{}, title:{}".format(name, title)

# import functools
# functools.partial(ff, title='hr')('sde')
