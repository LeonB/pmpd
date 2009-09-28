from twisted.protocols import basic
from server import MpdLayerServer
from player import MpdLayerPlayer

class MpdProtocol(basic.LineReceiver):
    #http://twistedmatrix.com/projects/core/documentation/howto/servers.html

    def connectionMade(self):
        self.server = MpdLayerServer(self.factory.mpd_server)
        self.player = MpdLayerPlayer(self.server.player)

        self.transport.write(self.first_connect())

    def connectionLost(self, reason):
        pass

    def dataReceived(self, data):
        words = data.split()

        if len(words) < 1: return self.transport.write(self.ok())
        methodname = words.pop(0)
        args = words

        if hasattr(self, methodname):
            method = getattr(self, methodname)
            self.transport.write(method(*args))

        return self.transport.write('ACK [5@0] {} unknown command "%s"\n' % methodname)

    def first_connect(self):
        return "OK MPD 0.14.0\n"

    def ok(self):
        return "OK\n"

    def error(self):
        return 'ACK'

    ### Querying MPD's status ###
    #http://www.musicpd.org/doc/protocol/ch02.html#id375210
    def clearerror(self):
        pass

    def status(self):
        return "status\n" \
            + "volume: 0\n" \
            + "repeat: 0\n" \
            + "random: 0\n" \
            + "playlist: 1\n" \
            + "playlistlength: 0\n" \
            + "xfade: 0\n" \
            + "state: %s\n" % self.player.state() \
            + self.ok()

    def currentsong(self):
        pass

    def idle(self):
        pass

    ### Controlling playback ###
    #http://www.musicpd.org/doc/protocol/ch02s03.html
    def next(self):
        self.player.next()
        return self.ok()

    def pause(self, int):
        self.player.pause()
        return self.ok()

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
