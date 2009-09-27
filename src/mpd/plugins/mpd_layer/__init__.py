#http://www.musicpd.org/doc/protocol/ch01s02.html
#@TODO: http://www.musicpd.org/doc/protocol/ch01s03.html (command lists)

import callbacks
from mpd.server import Server

from twisted.internet.protocol import Factory
from twisted.internet import reactor
from threading import Thread

from protocol import MpdProtocol

class MpdProtocolFactory(Factory):
    protocol = MpdProtocol

    def __init__(self, mpd_server):
        self.mpd_server = mpd_server

class MpdLayer(object):
    @classmethod
    def run(cls, server):
        server.log.debug("Started the mpd layer on port 8000")

        reactor.listenTCP(8000, MpdProtocolFactory(server))
        cls.thread = Thread(None, reactor.run, None, (), {'installSignalHandlers':0})
        cls.thread.start()


    @classmethod
    def stop(cls, server):
        print 'stopping....'
        try:
            reactor.callFromThread(reactor.stop) #huh?!?...
        except Exception:
            pass
        finally:
            if cls.thread and cls.thread.is_alive():
                cls.thread.join()

#callbacks.RegisterCallback(Server, 'before_run',
#    PermanentCallback(doit))
callbacks.RegisterCallback(Server, 'before_run', MpdLayer.run)
callbacks.RegisterCallback(Server, 'before_stop', MpdLayer.stop)