from subprocess import Popen, PIPE
import logging

logger = logging.getLogger(__name__)


def shell(*args, **kwargs):
    """
    there are two part of input parameters, the first part is
    shell command, second is options. e.g.
    shell('echo', 'hello', output=True). 'echo' and 'hello' is
    command, output is options

    available options:
    - output: if input present and value is true. return value
    will be a tuple (code, output), otherwise return only code
    """
    logger.info('runing  shell command %s' % repr(args))
    is_return_output = kwargs.get('output', False)
    process = Popen(args, stdout=PIPE)
    output, unused_err = process.communicate()
    retcode = process.poll()
    logger.info("shell command %s, retcode:%d, output: %s" % (repr(args), retcode, output))
    if is_return_output:
        return (retcode, output)
    else:
        return retcode

    # logger.info('runing shell command ' + repr(args))
    # return call(('sudo',) + args, stdout=sys.stdout, stderr=sys.stdout)


def host_is_live(remote_host):
    return shell('/bin/nc', '-z', remote_host, '22') == 0


def where_mount(device):
    with open('/proc/mounts') as f:
        for line in f:
            dev, mount_point = line.split(' ')[:2]
            if device == dev:
                return mount_point
            if device == mount_point:
                return dev
    return None


def umount(device):
    "path can be device e.g. /dev/xvda or mount point /local"
    if not where_mount(device):
        return True
    shell('/bin/fuser', '-m', '-k', '-TERM', device)
    if shell('/bin/umount', '-d', device) != 0:
        return False
    return True


def mount(device, mount_point):
    exist_mount_device = where_mount(mount_point)
    if exist_mount_device:
        logger.error('%s already was mounted by %s' % (mount_point, exist_mount_device))
        return False
    if shell('/bin/mount', device, mount_point) != 0:
        return False
    return True
