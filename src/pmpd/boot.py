from config import Config
from logger import Logger
import pmpd as Pmpd
import callbacks

class Boot:
    def __init__(self):
        self.setup_config()
        self.setup_logger()
        self.setup_callbacks()
        self.load_plugins()

    def setup_config(self):
        Pmpd.config = Config()

    def setup_logger(self):
        Pmpd.log = Logger()
        Pmpd.log.debug('booting...')

    def setup_callbacks(self):
        from player import Player
        callbacks.RegisterCallback(Player, 'play',
            lambda p: Pmpd.log.debug('Starting playback of %s' % p.current_track))

    def load_plugins(self):
        callbacks.RunCallbackChain(self, 'before_loading_plugins', Pmpd)

        for plugin in Pmpd.config.plugins:
            print plugin

        callbacks.RunCallbackChain(self, 'after_loading_plugins', Pmpd)