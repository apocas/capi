capi
====

capi is a log watcher and dispatcher.

It watches for changes in the specified logs and sends new entries to a redis database.

Its basically beaver https://github.com/josegonzalez/beaver on steroids, capi is daemonized, multithreaded and dependencies number decreased, only supporting redis.

Its perfect to use with your cPanel cluster + logstash setup.
Originally it was made to work on cPanel servers without any pain, but its applications are endeless.

##Usage:
```
git clone https://github.com/apocas/capi
cd capi; sh install.sh;
vi /etc/capid.conf
service capid restart
```

##Conf file (/etc/capid.conf) examples:

cPanel domlogs example and single file syslog example

```
[accesslogs]
#directory or file
type=directory

#directory to be watched
path=/usr/local/apache/domlogs/

#redis key pair
key=logs

#redis host, port and id
host=redis://127.0.0.1:6379/0

#file extensions to be ignored
ext=bytes,ftp,bkup


[messages]
type=file
path=/var/log/messages
key=logssyslog
host=redis://127.0.0.1:6379/0
```