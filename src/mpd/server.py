from config import Config
from logger import Logger
import mpd as MPD
import callbacks
import gobject

"""Hier komt alles in om de applicatie "echt" te laten draaien"""
#@TODO: misschien nog renamen naar app/server?

class Server:
    def __init__(self):
        self.setup_config()
        self.setup_logger()
        self.setup_callbacks()
        self.load_plugins()

    def setup_config(self):
        self.config = Config()

    def setup_logger(self):
        self.log = Logger(self.config.log)
        self.log.debug('booting...')

    def setup_callbacks(self):
        from player import Player
        callbacks.RegisterCallback(Player, 'play',
            lambda p: MPD.log.debug('Starting playback of %s' % p.current_track))

    def load_plugins(self):
        callbacks.RunCallbackChain(self, 'before_loading_plugins', MPD)

        for plugin in self.config.plugins:
            print plugin

        callbacks.RunCallbackChain(self, 'after_loading_plugins', MPD)

    def run(self):
        gobject.threads_init()
        self.loop = gobject.MainLoop()
        self.loop.run()

    def stop(self):
        self.loop.quit()