#!/usr/bin/env python3

from pwn import *
context.log_level = 'info'
from concurrent.futures import ThreadPoolExecutor, as_completed

site = 'https://portal.quick.htb/'
# gets the content of this url using a commandline HTTP3 client (quiche) as a UTF-8 decoded string.
# https://developers.cloudflare.com/http3/intro/http3-client/
def getUrl(url):
    context.log_level = 'error'
    client = process(['./quiche/target/debug/examples/http3-client', site+url])
    res = client.recvrepeat()
    client.close()
    return url, res.decode()


# Tries to find PDF documents in the docs folder using a wordlist.
# Uses multithreading to speed up the process.
def gothroughList():
    resP = log.progress('results: ')
    subP = log.progress('requesting: ')
    processes = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        file = open('/usr/share/seclists/Discovery/Web-Content/common.txt')
        lines = file.readlines()
        log.info('{} lines to check'.format(str(len(lines))))
        count = 1
        for line in lines:
            line = 'docs/' + line.strip() + '.pdf'
            subP.status(str(count))
            count += 1
            processes.append(executor.submit(getUrl, line))
    
    for task in as_completed(processes):
        url, res = task.result()
        resP.status(url)
        if '404 Not Found' not in res:
            log.info('url: {}'.format(url))
            log.info(res)

gothroughList()