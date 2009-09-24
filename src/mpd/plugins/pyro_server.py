import Pyro.core
import callbacks
from callbacks import PermanentCallback
from mpd.server import Server
from threading import Thread

class PyroServer(object):
    def __init__(self, player):
        Pyro.core.initServer(banner=0)
        PyroServer.daemon=Pyro.core.Daemon()
        PyroServer.daemon.connect(PyroPlayer(player), "pmpd")

        PyroServer.thread = Thread(None, self.run)
        PyroServer.thread.start()
        
    def run(self):
        try:
            PyroServer.daemon.requestLoop()
        finally:
            PyroServer.daemon.shutdown(True)

    @classmethod
    def stop(cls):
        print 'stopping pyro daemon'
        PyroServer.daemon.shutdown(True)

        print 'shutting down thread'
        PyroServer.thread.join()

        print 'done...'

class PyroPlayer(Pyro.core.ObjBase):
    def __init__(self, player):
        Pyro.core.ObjBase.__init__(self)
        self.player = player

    def __getattr__(self, attr):
        return getattr(self.player, attr)

callbacks.RegisterCallback(Server, 'after_setup_player',
    PermanentCallback(lambda s: s.log.debug('yep, after_setup_player is called')))

callbacks.RegisterCallback(Server, 'after_setup_player',
    PermanentCallback(lambda s: PyroServer(s.player)))

callbacks.RegisterCallback(Server, 'after_stop',
    PermanentCallback(lambda s: PyroServer.stop()))