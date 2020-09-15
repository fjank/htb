#!/usr/bin/env python3

# watching the server-status, to see if new unknown requests appear or not.

import requests
from pwn import *
def sendRequest():
    res = requests.get('http://10.10.10.186:9001/server-status')
    txt = res.text
    start = txt.index('<th>Request</th></tr>')
    end = txt.index('</table>')
    lines = txt[start+21:end].strip().split('\n\n')
    lines2 = set()
    for e in lines:
        estart = e.index('<td nowrap>')
        lines2.add(e[estart+11:-10].replace('</td><td nowrap>', ' '))
    return lines2


log.info('Registering initial URL\'s')
lines2 = sendRequest()
init_size = len(lines2)
for req in lines2:
    log.info(req)
log.info('Waiting for more equests')
while True:
    lines2.update(sendRequest())
    if len(lines2) != init_size:
        log.info('New requests arrived!')
        init_size = len(lines2)
        for req in lines2:
            log.info(req)
    sleep(1)
    