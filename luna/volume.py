from docker import Client as DockerClient
import traceback
import settings
from luna import linux
from luna.lina_client import LinaClient
from luna import util
import logging

logger = logging.getLogger(__name__)


class Run(object):

    def __init__(self, args):
        pass

    def pre_run(self):
        pass

    def post_run(self):
        pass


class Wait(object):

    def __init__(self, args):
        docker = DockerClient(base_url='unix://var/run/docker.sock',
                              version=settings.DOCKER_API_VERSION)
        self.volumes = []
        for container in args:
            try:
                container_info = docker.inspect_container(container)
                if not container_info['Volumes']:
                    continue
                for docker_path, local_path in container_info['Volumes'].items():
                    local_path = local_path.strip('/').split('/')
                    if local_path[0] == 'app_volume' and local_path[1] == 'ebs':
                        self.volumes.append((local_path[2], docker_path))
            except Exception:
                traceback.print_exc()

    def post_run(self):
        lina = LinaClient(settings.LINA_ENDPOINT)
        for app_id, volume_dir in self.volumes:
            app_volume = lina.get_app_volume(app_id, volume_dir)
            if not app_volume:
                continue
            if app_volume['volume_type'] != 'ebs':
                continue
            ebs_info = app_volume['volume_info']
            if ebs_info['status'] != 'attached':
                continue

            device = ebs_info['device']
            if not linux.umount(device):
                logger.error('failed to umount device %s' % device)
                continue

            ebs_volume_id = ebs_info['ebs_volume_id']
            logger.info("detach ebs volume %s" % ebs_volume_id)
            if not lina.detach_ebs_volume(ebs_volume_id):
                logger.error('failed to detach EBS volume %s' % ebs_volume_id)
            def _try():
                return lina.get_ebs_volume(ebs_info['ebs_volume_id'])

            def _check(ebs_info):
                return ebs_info['status'] == 'free'

            util.try_until(_try, _check, 3, 60)
