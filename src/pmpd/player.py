from attr import *
from playlist import Playlist
from player_backend import PlayerBackend
import callbacks

class Player(object):
    #attr_accessor :current_track, :history, :playlist, :current_track, :backend

    def __init__(self):
        from player_backends.gstreamer import Gstreamer
        self.playlist = Playlist()
        self.backend = PlayerBackend(self, Gstreamer)

        self.current_track = None

    def state(self):
        return self.backend.get_state()

    def next_track_as_current(self):
        self.current_track = self.playlist.get()

    def play(self):
    #if still playing, return nothing
        #if self.state == Player.PLAYING: return None
        #if self.state == Player.PAUSED: return self.backend.resume()
        if self.playlist.empty() and not self.current_track: return None

        if not self.current_track:
            self.next_track_as_current()

        self.backend.play(self.current_track.name) #Current track is set
        callbacks.RunCallbackChain(Player, 'play', self)

    def playing(self):
        return self.state() == 'playing'

    def register_callback(self, name, callback, permanent=False, priority=0):
        return callbacks.RegisterCallback(Player, name, callback, permanent, priority)