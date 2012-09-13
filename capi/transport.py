import datetime
import os
import redis
import urlparse
import socket

for mod in ['ujson', 'simplejson', 'jsonlib2', 'json']:
    try:
        json = __import__(mod)
    except ImportError:
        pass
    else:
        break

class RedisTransport(object):

    def __init__(self, args):
        self.current_host = socket.gethostname()
        redis_url = args.host
        _url = urlparse.urlparse(redis_url, scheme="redis")
        _, _, _db = _url.path.rpartition("/")


        self.redis = redis.StrictRedis(host=_url.hostname, port=_url.port, db=int(_db), socket_timeout=10)
        self.redis_namespace = args.key

    def callback(self, filename, lines):
        timestamp = datetime.datetime.now().isoformat()

        for line in lines:
            if len(line) > 20:
                aux = self.redis.lpush(
                    self.redis_namespace,
                    self.format(filename, timestamp, line)
                )

    def interrupt(self):
        return True

    def unhandled(self):
        return True

    def format(self, filename, timestamp, line):
        return json.dumps({
            '@source': "file://{0}{1}".format(self.current_host, filename),
            '@tags': [],
            '@fields': {},
            '@timestamp': timestamp,
            '@source_host': self.current_host,
            '@source_path': filename,
            '@message': line.strip(os.linesep),
        })
