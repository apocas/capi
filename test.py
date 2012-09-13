#!/usr/bin/env python
 
import sys, os, time, atexit
from capi import worker
from capi import transport
import datetime
import argparse
import errno
import urlparse
import ConfigParser
from signal import SIGTERM
from threading import Thread
 


class Workers(object):
        @staticmethod
        def create_worker(args):
                os.nice(19)
                transport = redis_transport.RedisTransport(args)
                if args.path == None:
                    l = worker.Worker(args, transport.callback)
                else:
                    l = worker.Worker(args, transport.callback, args.ext)
                l.loop()
 

threads = []
parser=ConfigParser.SafeConfigParser()
parser.read(['/etc/capid.conf'])
for section in parser.sections():
    class Object(object):
        pass

    args = Object()

    if parser.get(section, 'type') == 'file':
        args.files = [parser.get(section, 'path')]
        args.path = None
    elif parser.get(section, 'type') == 'directory':
        args.path = parser.get(section, 'path')
        args.files = None
        args.ext = parser.get(section, 'ext').split(",")
    args.key = parser.get(section, 'key')
    args.mode = "bind"
    args.host = parser.get(section, 'host')
    

    t1 = Thread(target=Workers.create_worker, args=(args,))
    t1.start()
    threads.append(t1)

for t in threads:
    t.join()
 