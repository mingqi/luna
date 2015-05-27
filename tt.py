from os.path import join, abspath
import sys

ROOT_DIR = abspath(join(__file__, '../'))
sys.path.insert(0, ROOT_DIR)

from luna import iptables
from luna import docker

# chain = iptables.get_chain('filter', 'FOR_TEST')
# rule = iptables.rule(src='192.168.0.1/255.255.255.0', target='ACCEPT')
# chain.append_rule(rule)
app_config = docker.service_configs('9f29f6b6-b7d9-48e8-a79c-295ab771f609')
print app_config
# print app_config['namespace']
# print app_config['service_name']

# service = docker.service_detail('vipertest', 'mysql')
# print service['default_domain_name']
# print service['instance_ports']

# print docker.add_allow_rule('1.1.1.2', 3320, '02:42:ac:11:00:00')

