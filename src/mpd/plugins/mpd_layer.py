#http://www.musicpd.org/doc/protocol/ch01s02.html
#@TODO: http://www.musicpd.org/doc/protocol/ch01s03.html (command lists)

import callbacks
from mpd.server import Server

from twisted.internet.protocol import Factory
from twisted.internet import reactor
from twisted.protocols import basic

from threading import Thread

class MpdProtocol(basic.LineReceiver):
    def connectionMade(self):
        self.server = self.factory.mpd_server
        self.player = self.server.player
        
        self.transport.write(self.first_connect())

    def dataReceived(self, data):
        self.transport.write(self.status())

    def first_connect(self):
        return "OK MPD 0.14.0\n"

    def ok(self):
        return 'OK'

    def error(self):
        return 'ACK'

    ### Querying MPD's status ###
    #http://www.musicpd.org/doc/protocol/ch02.html#id375210
    def clearerror(self):
        pass

    def status(self):
        return "status\n" \
            + "volume: 0\n" \
            + "repeat: 0" \
            + "random: 0\n" \
            + "playlist: 1\n" \
            + "playlistlength: 0\n" \
            + "xfade: 0\n" \
            + "state: stop\n" \
            "OK\n"

    def currentsong(self):
        pass

    def idle(self):
        pass

    ### Controlling playback ###
    #http://www.musicpd.org/doc/protocol/ch02s03.html

    ### The current playlist ###
    #http://www.musicpd.org/doc/protocol/ch02s04.html

    ### Stored playlists ###
    #http://www.musicpd.org/doc/protocol/ch02s05.html

    ### The music database ###
    #http://www.musicpd.org/doc/protocol/ch02s06.html

    ### Stickers ###
    #http://www.musicpd.org/doc/protocol/ch02s07.html

    ### Connection settings ###
    #http://www.musicpd.org/doc/protocol/ch02s08.html

    ### Audio output devices ###
    #http://www.musicpd.org/doc/protocol/ch02s09.html

    ### Reflection ###
    #http://www.musicpd.org/doc/protocol/ch02s10.html

class MpdProtocolFactory(Factory):
    protocol = MpdProtocol

    def __init__(self, mpd_server):
        self.mpd_server = mpd_server

class MpdLayer(object):
    @classmethod
    def run(cls, server):
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
