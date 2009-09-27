from twisted.protocols import basic
from server import MpdLayerServer
from player import MpdLayerPlayer

class MpdProtocol(basic.LineReceiver):
    def connectionMade(self):
        self.server = MpdLayerServer(self.factory.mpd_server)
        self.player = MpdLayerPlayer(self.server.player)

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
            + "repeat: 0\n" \
            + "random: 0\n" \
            + "playlist: 1\n" \
            + "playlistlength: 0\n" \
            + "xfade: 0\n" \
            + "state: %s\n" % self.player.state() \
            + "OK\n"

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
    