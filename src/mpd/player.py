from attr import *
from playlist import Playlist
from player_backend import PlayerBackend
import callbacks

class Player(object):
    #attr_accessor :current_track, :history, :playlist, :current_track, :backend
    attr_accessor(current_track = None)

    def __init__(self):
        from player_backends.gstreamer import Gstreamer
        self.playlist = Playlist()
        self.backend = PlayerBackend(self, Gstreamer)

    def state(self):
        return self.backend.get_state()

    def schedule_next_track(self):
        callbacks.RunCallbackChain(Player, 'scheduling_new_track', self)
        self.remove_current_track()

        if self.playlist.empty():
            #print 'nope, no new track'
            self.stop()
            return False

        return self.next_track_as_current()

    def next_track_as_current(self):
        callbacks.RunCallbackChain(Player, 'next_track', self)
        self.current_track = self.playlist.get()
        #print 'New track: ' + self.current_track.name

    def remove_current_track(self):
        self.current_track = None

    def play(self):
        #if still playing, return nothing
        if (self.state() == 'playing'): return False
        if (self.state() == 'paused'): return self.resume()
        if (self.playlist.empty() and not self.current_track): return None

        if not self.current_track:
            self.next_track_as_current()

        print 'play'

        result = self.backend.play(self.current_track) #Current track is set
        callbacks.RunCallbackChain(Player, 'play', self)
        return result

    def pause(self):
        if self.playing():
            return self.backend.pause()
        elif self.paused():
            return self.resume()

    def resume(self):
        return self.backend.resume()

    def stop(self):
        self.backend.stop()
        result = self.remove_current_track()
        callbacks.RunCallbackChain(Player, 'stop', self)
        return result

    def next(self):
        self.schedule_next_track()
        return self.backend.play(self.current_track) #Current track is set

    def playing(self):
        return self.state() == 'playing'

    def paused(self):
        return self.state() == 'paused'

    def stopped(self):
        return self.state() == 'stopped'

    def register_callback(self, name, callback, permanent=False, priority=0):
        return callbacks.RegisterCallback(Player, name, callback, permanent, priority)