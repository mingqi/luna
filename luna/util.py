import time
import json
import boto.utils
import socket


def try_until(try_fn, check_fn, sleep_sec, timeout_sec):
    time.sleep(sleep_sec)
    start_time = time.time()
    while True:
        result = try_fn()
        if check_fn(result):
            return result
        else:
            curr = time.time()
            if timeout_sec > 0 and curr - start_time > timeout_sec:
                raise Exception("timeout for %i" % timeout_sec)
            else:
                time.sleep(sleep_sec)


def my_instance_id():
    meta = boto.utils.get_instance_metadata()
    if not meta:
        return None
    return meta['instance-id']


def flush_ops_logs(path, app_id, instance_id, container_name, content, log_type):
    # This func is not Thread-safey.
    data = {
        "id": "{:.10f}".format(time.time()).replace('.', ''),
        "time": int("{:.6f}".format(time.time()).replace('.', '')),
        'log_type': log_type,
        'app_id': app_id,
        'instance_id': instance_id,
        'log_data': content,
        'log_level': 0,
        "machine": socket.gethostname(),
        'container_name': container_name
    }
    fp = open(path, 'a+')
    fp.write(json.dumps(data))
    fp.close()