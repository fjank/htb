#!/usr/bin/env python3

# since gobuster, dirb and wfuzz is not too happy about the SSL certificate, 
# I have written my own multithreaded fuzzer/dirbuster.

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from pwn import *
from concurrent.futures import ThreadPoolExecutor, as_completed

p=log.progress('Wordlist:')
def checkurl(url):
    try:
        html = requests.head(url, verify=False)
        p.status(f'{url} - {html.status_code}')
        if html.status_code != 404:
            log.info(f'{url} - {html.status_code}')
        return html.status_code, url
    except requests.exceptions.RequestException as e:
       return 500, e

def runner():
    threads= []
    with open('dirbustlist.txt') as wl:
        with ThreadPoolExecutor(max_workers=20) as executor:
            for line in [line.strip() for line in wl]:
                threads.append(executor.submit(checkurl, f'https://ssl.travel.htb/{line}'))
           
    for task in as_completed(threads):
        code, url = task.result()
      
runner()
