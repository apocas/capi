import os
import stat
import time
import errno

class Worker(object):

    def __init__(self, args, callback, extensions = None):
        self.files_map = {}
        self.callback = callback
        self.extensions = extensions
        self.config = args

        if self.config.path is not None:
            self.folder = os.path.realpath(args.path)
            assert os.path.isdir(self.folder), "%s does not exists" % self.folder
        assert callable(callback)
        self.update_files()
        for id, file in self.files_map.iteritems():
            file.seek(os.path.getsize(file.name))

    def __del__(self):
        self.close()

    def loop(self, interval=0.1, async=False):
        while 1:
            self.update_files()
            for fid, file in list(self.files_map.iteritems()):
                self.readfile(file)
            if async:
                return
            time.sleep(interval)

    def listdir(self):
        ls = os.listdir(self.folder)

        if self.extensions:
            return [ff for ff in ls if any(x in ff for x in self.extensions) == False]
        else:
            return ls

    @staticmethod
    def tail(fname, window):
        try:
            f = open(fname, 'r')
        except IOError, err:
            if err.errno == errno.ENOENT:
                return []
            else:
                raise
        else:
            BUFSIZ = 1024
            f.seek(0, os.SEEK_END)
            fsize = f.tell()
            block = -1
            data = ""
            exit = False
            while not exit:
                step = (block * BUFSIZ)
                if abs(step) >= fsize:
                    f.seek(0)
                    exit = True
                else:
                    f.seek(step, os.SEEK_END)
                data = f.read().strip()
                if data.count('\n') >= window:
                    break
                else:
                    block -= 1
            return data.splitlines()[-window:]

    def update_files(self):
        ls = []
        files = []
        if self.config.files is not None:
            for name in self.config.files:
                files.append(os.path.realpath(name))
        else:
            for name in self.listdir():
                files.append(os.path.realpath(os.path.join(self.folder, name)))

        for absname in files:
            try:
                st = os.stat(absname)
            except EnvironmentError, err:
                if err.errno != errno.ENOENT:
                    raise
            else:
                if not stat.S_ISREG(st.st_mode):
                    continue
                fid = self.get_file_id(st)
                ls.append((fid, absname))

        for fid, file in list(self.files_map.iteritems()):
            try:
                st = os.stat(file.name)
            except EnvironmentError, err:
                if err.errno == errno.ENOENT:
                    self.unwatch(file, fid)
                else:
                    raise
            else:
                if fid != self.get_file_id(st):
                    self.unwatch(file, fid)
                    self.watch(file.name)

        for fid, fname in ls:
            if fid not in self.files_map:
                self.watch(fname)

    def readfile(self, file):
        lines = file.readlines()
        if lines:
            self.callback(file.name, lines)

    def watch(self, fname):
        try:
            file = open(fname, "r")
            fid = self.get_file_id(os.stat(fname))
        except EnvironmentError, err:
            if err.errno != errno.ENOENT:
                raise
        else:
            print "[{0}] - watching logfile {1}".format(fid, fname)
            self.files_map[fid] = file

    def unwatch(self, file, fid):
        lines = self.readfile(file)
        print "[{0}] - un-watching logfile {1}".format(fid, file.name)
        del self.files_map[fid]
        if lines:
            self.callback(file.name, lines)

    @staticmethod
    def get_file_id(st):
        return "%xg%x" % (st.st_dev, st.st_ino)

    def close(self):
        for id, file in self.files_map.iteritems():
            file.close()
        self.files_map.clear()
