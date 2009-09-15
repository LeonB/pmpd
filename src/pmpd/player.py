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

    def schedule_next_track(self):
        print 'scheduling new track'
        self.remove_current_track()

        print self.playlist.empty()
        if self.playlist.empty():
            self.stop()
            return False

        #self.schedule_next_track()
        return self.next_track_as_current()

    def next_track_as_current(self):
        self.current_track = self.playlist.get()
        print 'New track: ' + self.current_track.name

    def remove_current_track(self):
        self.current_track = None

    def play(self):
    #if still playing, return nothing
        #if self.state == Player.PLAYING: return None
        #if self.state == Player.PAUSED: return self.backend.resume()
        if self.playlist.empty() and not self.current_track: return None

        if not self.current_track:
            self.next_track_as_current()

        self.backend.play(self.current_track.name) #Current track is set
        callbacks.RunCallbackChain(Player, 'play', self)

    def pause(self):
        if self.playing():
            self.backend.pause()
        elif self.paused():
            self.backend.play()

    def stop(self):
        self.backend.stop()

    def next(self):
        self.schedule_next_track()
        self.play()

    def playing(self):
        return self.state() == 'playing'

    def paused(self):
        return self.state() == 'paused'

    def register_callback(self, name, callback, permanent=False, priority=0):
        return callbacks.RegisterCallback(Player, name, callback, permanent, priority)