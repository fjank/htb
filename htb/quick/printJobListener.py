#!/usr/bin/env python3

# Waits for a job to appear in the jobs folder, as soon as a job appear, 
# the job is replaced with a symlink to the private SSH key, 
# so that is sent to the printer instead. (we are in control of the printer)
import glob, os, time
def getList():
    return glob.glob('/var/www/jobs/*')

while True:
    list = getList()
    if len(list) > 0:
        time.sleep(0.1)
        print(list[0])
        os.remove(list[0])
        os.symlink('/home/srvadm/.ssh/id_rsa', list[0])
        exit()