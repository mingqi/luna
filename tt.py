from os.path import join, abspath
import sys

ROOT_DIR = abspath(join(__file__, '../'))
sys.path.insert(0, ROOT_DIR)

from luna import iptables

print iptables.create_chain('filter', 'FOR_TEST')
