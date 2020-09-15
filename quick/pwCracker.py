#!/usr/bin/env python3

# custom password cracker. We have the hash, and the algorithm, but its not supported
# in hashcat or john, so we do it manually. hashlib.md5(crypt.crypt(pw, 'fa').encode()).hexdigest()

import crypt, hashlib
from pwn import *

expectedHash = 'e626d51f8fbfd1124fdea88396c35d05'

p = log.progress('Cracking password: ')
file = open('/usr/share/wordlists/rockyou.txt', encoding='iso-8859-1')
lines = file.readlines()
tot = len(lines)
count = 1
log.info('Total passwords: ' + str(tot))
for line in lines:
    line = line.strip()
    p.status(str(int(count*100/tot)) + '%: ' + line)
    count += 1
    cry = crypt.crypt(line, 'fa').encode()
    md = hashlib.md5(cry).hexdigest()
    if md == expectedHash:
        p.success('Found! [{}]'.format(line))
        exit()
