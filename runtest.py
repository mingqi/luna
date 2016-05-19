#!/usr/bin/env python

from os import path
import sys
import unittest
from luna.tests import test_wrapper

import logging

FORMAT = '%(asctime)-15s %(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO, stream=sys.stdout)

logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())

ROOT_DIR = path.dirname(__file__)
sys.path.insert(0, ROOT_DIR)
# unittest.main(module='lina.tests.test_workflow')
# unittest.main(module='lina.tests.test_volume')


suite = unittest.TestSuite()
suite.addTest(unittest.TestLoader().loadTestsFromModule(test_wrapper))
# suite.addTest(unittest.TestLoader().loadTestsFromModule(test_volume))
unittest.TextTestRunner(verbosity=2).run(suite)
