
from os.path import join, abspath
import sys
from pprint import pprint
import functools

ROOT_DIR = abspath(join(__file__, '../'))
sys.path.insert(0, ROOT_DIR)


from luna import util
from luna import docker_cli_parser



# args = util.parse_run_cli(sys.argv[1:])
# print args

# print docker_cli_parser.run("-it -d -c -m 536870912 -e mesos_task_id=ct:1433994437746:0:delete_cluster-xdzhang-1: -e CHRONOS_JOB_OWNER= -e CHRONOS_JOB_NAME=delete_cluster-xdzhang-1 -e HOST=ip-172-31-38-206.us-west-2.compute.internal -e CHRONOS_RESOURCE_MEM=512.0 -e CHRONOS_RESOURCE_CPU=0.5 -e CHRONOS_RESOURCE_DISK=256.0 -e NEVERMORE_ACTION_TYPE=Delete -e NEVERMORE_EC2_REGION=us-west-2 -e NEVERMORE_EC2_KEY=AKIAJJ34GNQKWTSP4Z5Q -e NEVERMORE_EC2_SECRET=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 -e NEVERMORE_TAG_PATTERN=xdzhang_cluster-xdzhang-1 -e MESOS_SANDBOX=/mnt/mesos/sandbox --net host --entrypoint /bin/sh --name mesos-38f7dc5f-e2d7-4ff4-932c-003b421f064e index.alauda.io/mathildetech/nevermore:latest -c /bin/bash -c /nevermore/nevermore.sh".split())
import logging

FORMAT = '%(levelname)-6s %(asctime)-15s %(name)s: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG, stream=sys.stdout)


logger = logging.getLogger(__name__)
logger.debug('this is debug')
logger.info('this is info')
logger.error('this is error')
# print 'aa'
