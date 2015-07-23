import time
import boto.utils


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
