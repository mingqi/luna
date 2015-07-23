from docker import Client as DockerClient
import traceback
import os
import errno
from os import path
import settings
from luna import linux
from luna.lina_client import LinaClient
from luna import util
import logging
from luna import docker_cli_parser

logger = logging.getLogger(__name__)


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def wait_volume_available(app_id, app_volume_dir):
    client = LinaClient(settings.LINA_ENDPOINT)

    def _try_fn():
        return client.get_app_volume(app_id, app_volume_dir)

    def _check_fn(app_volume):
        if app_volume['status'] == 'error':
            raise Exception('failed to create volume')
        return app_volume['status'] == 'available'

    app_volume = client.get_app_volume(app_id, app_volume_dir)
    if not app_volume:
        raise Exception('app volume <%s, %s> is not exists' % (app_id, app_volume_dir))
    return util.try_until(_try_fn, _check_fn, 10, 300)


def attach_ebs_volume(ebs_volume_id):
    logger.info('attaching volume for %s' % ebs_volume_id)
    client = LinaClient(settings.LINA_ENDPOINT)
    local_instance_id = util.my_instance_id()
    client.attach_ebs_volume(ebs_volume_id, local_instance_id)

    def _try_fn():
        return client.get_ebs_volume(ebs_volume_id)

    def _check_fn(ebs_volume):
        return ebs_volume['status'] == 'attached' and \
             ebs_volume['ec2_instance_id'] == local_instance_id

    ebs_volume = util.try_until(_try_fn, _check_fn, 3, 120)
    return ebs_volume['device']


class Run(object):

    def __init__(self, args):
        opts, args = docker_cli_parser.run(args)
        app_id = None
        for env in opts.get('env', []):
            name, value = env.split('=')
            if name == 'MARATHON_APP_ID':
                app_id = value.strip('/')
        self.app_volumes = []
        if app_id:
            for volume in opts.get('volume', []):
                local_path, container_path = volume.split(':')
                local_path = local_path.rstrip('/')
                container_path = container_path.rstrip('/')
                if local_path != '/app_volume/ebs/%s%s/volume' % (app_id, container_path):
                    raise Exception('volume path is not match standard: %s' % volume)
                self.app_volumes.append((app_id, container_path))

    def pre_run(self):
        for app_id, app_volume_dir in self.app_volumes:
            mount_point = '/app_volume/ebs/%s%s' % (app_id, app_volume_dir)
            mkdir_p(mount_point)
            logger.info('starting to mount <%s,%s> at %s' % (app_id, app_volume_dir, mount_point))
            app_volume = wait_volume_available(app_id, app_volume_dir)
            ebs_volume_id = app_volume['volume_info']['ebs_volume_id']
            device = attach_ebs_volume(ebs_volume_id)

            curr_mounted_point = linux.where_mount(device)
            if curr_mounted_point:
                if curr_mounted_point == mount_point:
                    logger.info('device already been mounting on %s, \
                        no need to mount it' % curr_mounted_point)
                    continue
                else:
                    linux.umount(device)

            curr_mounted_device = linux.where_mount(mount_point)
            if curr_mounted_device:
                logger.info('%s already mount by %s, umounting it' % (mount_point, curr_mounted_device))
                if not linux.umount(curr_mounted_device):
                    raise Exception('failed to umount occupied mount point')
            if not linux.mount(device, mount_point):
                raise Exception('faile to mount device %s on %s' % (device, mount_point))

            volume_dir = path.join(mount_point, 'volume')
            if not path.exists(volume_dir):
                # os.makedirs(volume_dir)
                raise Exception('volume does not have /volume directory')


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
