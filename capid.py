#!/usr/bin/env python
 
import sys, os, time, atexit
from capi import worker
from capi import transport
from capi import redis_transport
import datetime
import argparse
import errno
import urlparse
from signal import SIGTERM
from threading import Thread
 
class Daemon:

        def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
                self.stdin = stdin
                self.stdout = stdout
                self.stderr = stderr
                self.pidfile = pidfile
       
        def daemonize(self):
                try:
                        pid = os.fork()
                        if pid > 0:
                                sys.exit(0)
                except OSError, e:
                        sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
                        sys.exit(1)
       
                os.chdir("/")
                os.setsid()
                os.umask(0)
       
                try:
                        pid = os.fork()
                        if pid > 0:
                                sys.exit(0)
                except OSError, e:
                        sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
                        sys.exit(1)
       
                sys.stdout.flush()
                sys.stderr.flush()
                si = file(self.stdin, 'r')
                so = file(self.stdout, 'a+')
                se = file(self.stderr, 'a+', 0)
                os.dup2(si.fileno(), sys.stdin.fileno())
                os.dup2(so.fileno(), sys.stdout.fileno())
                os.dup2(se.fileno(), sys.stderr.fileno())
       
                atexit.register(self.delpid)
                pid = str(os.getpid())
                file(self.pidfile,'w+').write("%s\n" % pid)
       
        def delpid(self):
                os.remove(self.pidfile)
 
        def start(self):
                try:
                        pf = file(self.pidfile,'r')
                        pid = int(pf.read().strip())
                        pf.close()
                except IOError:
                        pid = None
       
                if pid:
                        message = "pidfile %s already exist. Daemon already running?\n"
                        sys.stderr.write(message % self.pidfile)
                        sys.exit(1)
                
                self.daemonize()
                self.run()
 
        def stop(self):
                try:
                        pf = file(self.pidfile,'r')
                        pid = int(pf.read().strip())
                        pf.close()
                except IOError:
                        pid = None
       
                if not pid:
                        message = "pidfile %s does not exist. Daemon not running?\n"
                        sys.stderr.write(message % self.pidfile)
                        return
     
                try:
                        while 1:
                                os.kill(pid, SIGTERM)
                                time.sleep(0.1)
                except OSError, err:
                        err = str(err)
                        if err.find("No such process") > 0:
                                if os.path.exists(self.pidfile):
                                        os.remove(self.pidfile)
                        else:
                                print str(err)
                                sys.exit(1)
 
        def restart(self):
                self.stop()
                self.start()
 
        def run(self):


class Workers(object):
        @staticmethod
        def create_worker(args):
                os.nice(19)
                transport = redis_transport.RedisTransport(args)
                l = worker.Worker(args, transport.callback)
                l.loop()
 
class MyDaemon(Daemon):

        def run(self):
                parser=ConfigParser.SafeConfigParser()
                parser.read(['/etc/capid.conf'])
                for section in parser.sections():
                    class Object(object):
                        pass

                    args = Object()
                    
                    if(parser.get(section, 'type') == "file")
                        args.files = [parser.get(section, 'path')]
                    elif (parser.get(section, 'type') == "directory")
                        args.path = parser.get(section, 'path')
                    args.key = parser.get(section, 'key')
                    args.mode = "bind"
                    args.host = parser.get(section, 'host')

                    t1 = Thread(target=Workers.create_worker(args), args=())
                    t1.start()
                    t1.join()
 
if __name__ == "__main__":
        daemon = MyDaemon('/tmp/capid.pid')
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        daemon.start()
                elif 'stop' == sys.argv[1]:
                        daemon.stop()
                elif 'restart' == sys.argv[1]:
                        daemon.restart()
                else:
                        print "Unknown command"
                        sys.exit(2)
                sys.exit(0)
        else:
                print "usage: %s start|stop|restart" % sys.argv[0]
                sys.exit(2)
