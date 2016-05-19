import requests
import json


class LinaCallException(Exception):

    def __init__(self, status_code, message):
        super(Exception, self).__init__()
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return repr('code: %d, message: %s' % (self.status_code, self.message))


class LinaClient(object):

    def __init__(self, host=None):
        self.host = host

    def get_app_volume(self, app_id, app_volume_dir):
        params = {
            'app_id': app_id,
            'app_volume_dir': app_volume_dir
        }
        r = requests.get('http://%s/api/v1/volumes' % self.host, params=params)
        if r.status_code == 404:
            return None

        if r.status_code >= 500:
            raise LinaCallException(r.status_code, r.text)

        return r.json()

    def get_ebs_volume(self, ebs_volume_id):
        r = requests.get('http://%s/api/v1/volumes/ebs/%s' %
                         (self.host, ebs_volume_id))
        if r.status_code == 404:
            return None

        if r.status_code >= 500:
            raise LinaCallException(r.status_code, r.text)

        return r.json()

    def create_app_volume(self, app_id, app_volume_dir,
                          size_gb, volume_type='ebs', snapshot_id=None):
        headers = {'content-type': 'application/json'}
        payload = {
            'app_id': app_id,
            'app_volume_dir': app_volume_dir,
            'size_gb': size_gb,
            'volume_type': volume_type
        }

        if snapshot_id:
            payload['snapshot_id'] = snapshot_id

        r = requests.post('http://%s/api/v1/volumes' % self.host,
                          data=json.dumps(payload), headers=headers)

        if r.status_code == 200:
            return r.json()

        raise LinaCallException(r.status_code, r.text)

    def attach_ebs_volume(self, ebs_volume_id, ec2_instance_id):
        params = {
            'ec2_instance_id': ec2_instance_id
        }
        headers = {'content-type': 'application/json'}
        r = requests.put('http://%s/api/v1/volumes/ebs/%s/attach' % (self.host, ebs_volume_id),
                         params=params,
                         headers=headers)

        if r.status_code == 200:
            return r.json()

        raise LinaCallException(r.status_code, r.text)

    def detach_ebs_volume(self, ebs_volume_id):
        headers = {'content-type': 'application/json'}
        r = requests.put('http://%s/api/v1/volumes/ebs/%s/detach' %
                         (self.host, ebs_volume_id),
                         headers=headers)

        if r.status_code == 200:
            return r.json()

        raise LinaCallException(r.status_code, r.text)

    def delete_app_volume(self, app_id, app_volume_dir):
        params = {
            'app_id': app_id,
            'app_volume_dir': app_volume_dir
        }
        headers = {'content-type': 'application/json'}
        r = requests.delete('http://%s/api/v1/volumes' % (self.host,),
                            params=params, headers=headers)
        if r.status_code == 204:
            return True
        raise LinaCallException(r.status_code, r.text)

    def create_snapshot(self, app_id, app_volume_dir, namespace, name):
        headers = {'content-type': 'application/json'}
        payload = {
            'app_id': app_id,
            'app_volume_dir': app_volume_dir,
            'namespace': namespace,
            'name': name
        }
        r = requests.post('http://%s/api/v1/snapshots' %
                          self.host, headers=headers, data=json.dumps(payload))

        if r.status_code == 200:
            return r.json()

        raise LinaCallException(r.status_code, r.text)

    def get_snapshot(self, snapshot_id):
        headers = {'content-type': 'application/json'}
        r = requests.get('http://%s/api/v1/snapshots/%s' %
                         (self.host, snapshot_id), headers=headers)
        if r.status_code == 404:
            return None

        if r.status_code == 200:
            return r.json()

        raise LinaCallException(r.status_code, r.text)

    def delete_snapshot(self, snapshot_id):
        headers = {'content-type': 'application/json'}
        r = requests.delete('http://%s/api/v1/snapshots/%s' %
                            (self.host, snapshot_id), headers=headers)

        if r.status_code == 204:
            return True

        raise LinaCallException(r.status_code, r.text)

    def recover_volume(self, app_id, app_volume_dir, snapshot_id):
        headers = {'content-type': 'application/json'}
        payload = {
            'app_id': app_id,
            'app_volume_dir': app_volume_dir,
            'snapshot_id': snapshot_id
        }

        r = requests.put('http://%s/api/v1/volumes/_recover' % self.host,
                         data=json.dumps(payload), headers=headers)

        if r.status_code == 200:
            return r.json()

        raise LinaCallException(r.status_code, r.text)
