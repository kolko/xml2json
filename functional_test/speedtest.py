#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import datetime
import subprocess


ITERS = 10000
if len(sys.argv) > 1:
    ITERS = int(sys.argv[1])


p = subprocess.Popen(['python', '../xml2json.py'], stdin=subprocess.PIPE, stdout=open('/dev/null', 'w'))
dt_start = datetime.datetime.now()
p.stdin.write('<?xml version="1.1" encoding="UTF-8" ?><books>')
progress_procent = ''
for x in xrange(ITERS):
    cur_progress_procent = '{0:.0f}'.format(x/(ITERS/100.0))
    if cur_progress_procent != progress_procent:
        progress_procent = cur_progress_procent
        print '{0}% '.format(progress_procent),
    p.stdin.write('''<book isbn="9780907486862">
           <author>Conan Doyle</author>
           <title>Sherlock Holmes: Complete Illustrated Stories</title>
           <tags>
             <tag>cool</tag>
             <tag>classic</tag>
           </tags>
         </book>''')
p.stdin.write('</books>')
p.stdin.close()
dt_end = datetime.datetime.now()
print
print 'For {0} iters time: {1}'.format(ITERS, dt_end-dt_start)