#from threading import Thread
import thread
from attr import *

class PlayerBackend(object):
    attr_accessor(state = 'stopped')

    def __init__(self, player, Backend):
        self.player = player
        self.backend = Backend(self.player)

    def pause(self):
        ''

    def play(self, uri):
        self.state = 'playing'
        #self.backend.play(uri)
        #self.thread = Thread(None, self.backend.play, uri)
        #self.thread.start()
        thread.start_new_thread(self.backend.play, (uri,))

    def stop(self):
        ''