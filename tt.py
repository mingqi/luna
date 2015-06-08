
from os.path import join, abspath
import sys
from pprint import pprint
import functools

ROOT_DIR = abspath(join(__file__, '../'))
sys.path.insert(0, ROOT_DIR)


from docopt import docopt, DocoptExit
from luna import util


args = util.parse_run_cli(sys.argv[1:])
print args