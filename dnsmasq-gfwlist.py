#!/usr/bin/env python
#coding=utf-8
#
# Generate a list of dnsmasq rules with ipset and easylist to block AD for Router
# author Meteoral
# Ref http://www.shuyz.com
# Ref https://code.google.com/p/autoproxy-gfwlist/wiki/Rules

import urllib2
import re
import os
import datetime
import base64
import shutil
import time
import commands

mydnsip = '127.0.0.1'
mydnsport = '5454'
cndns = '114.114.114.114'
filtername = 'gfwlist'
homedir = '.'
rulesfile = homedir + '/gfwlist.conf'
adbfile = homedir + '/adblist.conf'

# the url of gfwlist
baseurl = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'
# match comments/title/whitelist/ip address
comment_pattern = '^\!|\[|^@@|^\d+\.\d+\.\d+\.\d+'
domain_pattern = '([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*'
date_pattern = 'Last Modified: (.*) [+-]0[0-9]00$'
tmpfile = '/tmp/gfwlisttmp'
# do not write to router internal flash directly
outfile = '/tmp/gfwlist.conf'

fs =  file(outfile, 'w')
fs.write('# gfw list ipset rules for dnsmasq\n')
fs.write('# by Meteoral\n')
fs.write('# E-mail : mail@liuqingwei.com\n')
fs.write('# Web : https://liuqingwei.com\n')
fs.write('# created on ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
print 'fetching list...'
content = urllib2.urlopen(baseurl, timeout=15).read().decode('base64')
# write the decoded content to file then read line by line
tfs = open(tmpfile, 'w')
tfs.write(content)
tfs.close()
tfs = open(tmpfile, 'r')
print 'page content fetched, analysis...'
# remember all blocked domains, in case of duplicate records
domainlist = []
for line in tfs.readlines():
        if re.findall(comment_pattern, line):
                date = re.findall(date_pattern, line)
                if date:
                    dates = time.strptime(date[0], "%a, %d %b %Y %H:%M:%S")
                    dates = time.strftime("%Y-%m-%d %H:%M:%S",dates)
                    fs.write('# updated list on ' + dates + '\n\n# gfwlist \n')
                else:
                    print 'this is a comment line: ' + line
                    #fs.write('#' + line)
        else:
                domain = re.findall(domain_pattern, line)
                if domain:
                        try:
                                found = domainlist.index(domain[0])
                                print domain[0] + ' exists.'
                        except ValueError:
                                print 'saving ' + domain[0]
                                domainlist.append(domain[0])
                                fs.write('server=/.%s/%s#%s\n'%(domain[0],mydnsip,mydnsport))
                                fs.write('ipset=/.%s/%s\n'%(domain[0],filtername))
                else:
                        print 'no valid domain in this line: ' + line

fs.write('\n# patch gfwlist\n')
fs.write('server=/.google.com.hk/%s#%s\n'%(mydnsip,mydnsport))
fs.write('ipset=/.google.com.hk/%s\n'%filtername)
fs.write('server=/.amazonaws.com/%s#%s\n'%(mydnsip,mydnsport))
fs.write('ipset=/.amazonaws.com/%s\n'%filtername)
tfs.close()
fs.close();

print 'moving generated file to dnsmasg directory'
shutil.move(outfile, rulesfile)
print 'generate gfwlist finish!'
print 'fetching easylist file'
print os.popen("wget --no-check-certificate -qO - https://easylist-downloads.adblockplus.org/easylistchina+easylist.txt | grep ^\|\|[^\*]*\^$ | sed -e 's:||:address\=\/:' -e 's:\^:/127\.0\.0\.1:' > " + adbfile).read()
print os.popen("echo 'address=/de.pandora.xiaomi.com/127.0.0.1' >> " + adbfile).read()
print os.popen("echo 'address=/mishop.pandora.xiaomi.com/127.0.0.1' >> " + adbfile).read()
print os.popen("echo 'address=/auth.api.gitv.tv/127.0.0.1' >> " + adbfile).read()
print os.popen("echo 'address=/misc.pandora.xiaomi.com/127.0.0.1' >> " + adbfile).read()
print os.popen("echo 'address=/tvapi.kuyun.com/127.0.0.1' >> " + adbfile).read()
print os.popen("echo 'address=/data.mistat.xiaomi.com/127.0.0.1' >> " + adbfile).read()
print os.popen("echo 'address=/tv.aiseet.atianqi.com/127.0.0.1' >> " + adbfile).read()
print os.popen("echo 'address=/vv.play.aiseet.atianqi.com/127.0.0.1' >> " + adbfile).read()
print os.popen("echo 'address=/gallery.pandora.xiaomi.com/127.0.0.1' >> " + adbfile).read()
print os.popen("echo 'address=/config.kuyun.com/127.0.0.1' >> " + adbfile).read()
print os.popen("echo 'address=/bss.pandora.xiaomi.com/127.0.0.1' >> " + adbfile).read()
print os.popen("echo 'address=/o2o.api.xiaomi.com/127.0.0.1' >> " + adbfile).read()
print os.popen("echo 'address=/dvb.pandora.xiaomi.com/127.0.0.1' >> " + adbfile).read()
print os.popen("echo 'address=/alog.umeng.com/127.0.0.1' >> " + adbfile).read()
print os.popen("echo 'address=/pandora.mi.com/127.0.0.1' >> " + adbfile).read()
print os.popen("echo 'address=/api.ad.xiaomi.com/127.0.0.1' >> " + adbfile).read()
print os.popen("echo 'address=/tvapi.kuyun.com/127.0.0.1' >> " + adbfile).read()
print os.popen("echo 'address=/sdkconfig.ad.xiaomi.com/127.0.0.1' >> " + adbfile).read()
print os.popen("echo 'address=/assistant.pandora.xiaomi.com/127.0.0.1' >> " + adbfile).read()
print os.popen("echo 'address=/tracking.miui.com/127.0.0.1' >> " + adbfile).read()
print os.popen("echo 'address=/misc.pandora.xiaomi.com/127.0.0.1' >> " + adbfile).read()
print os.popen("echo 'address=/gvod.aiseejapp.atianqi.com/127.0.0.1' >> " + adbfile).read()
print os.popen("echo 'address=/omgmta.play.aiseet.atianqi.com/127.0.0.1' >> " + adbfile).read()
print os.popen("echo 'address=/jellyfish.pandora.xiaomi.com/127.0.0.1' >> " + adbfile).read()
print os.popen("echo 'address=/starfish.pandora.xiaomi.com/127.0.0.1' >> " + adbfile).read()
print os.popen("echo 'address=/misc.in.duokanbox.com/127.0.0.1' >> " + adbfile).read()

print 'done!'
