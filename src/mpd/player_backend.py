#from threading import Thread
import thread
from attr import *

class PlayerBackend(object):
    attr_accessor(state = 'stopped', thread = None)

    def __init__(self, player, Backend):
        self.player = player
        self.backend = Backend(self.player)

    def play(self, uri):
        self.state = 'playing'
        self.backend.play(uri)
        #self.thread = Thread(None, self.backend.play, uri)
        #self.thread.start()
        #self.thread = thread.start_new_thread(self.backend.play, (uri,))

    def pause(self):
        self.state = 'paused'
        self.backend.pause()

    def stop(self):
        print 'stopping...'
        self.backend.stop()
        self.state = 'stopped'