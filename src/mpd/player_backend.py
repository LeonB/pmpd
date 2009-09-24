#from threading import Thread
#import thread
from threading import Thread
from multiprocessing import Process
#import threading
from attr import *

class PlayerBackend(object):
    attr_accessor(state = 'stopped', thread = None)

    def __init__(self, player, Backend):
        self.player = player
        self.__backend = Backend
        self.backend = self.__backend(self.player)

    def play(self, track):
        self.state = 'playing'
        
        if self.thread:
            self.thread.join()

        self.thread = Thread(None, self.backend.play, None, (track,))
        #self.thread = Process(target=self.backend.play, args=(track,))
        self.thread.start()

    def resume(self):
        self.state = 'playing'
        return self.backend.resume()

    def pause(self):
        self.state = 'paused'
        return self.backend.pause()

    def stop(self):
        self.backend.stop() #this should end the thread
        self.state = 'stopped'