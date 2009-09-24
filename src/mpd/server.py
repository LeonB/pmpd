from mpd.player_backend import PlayerBackend
from config import Config
from logger import Logger
from player import Player
import callbacks
from callbacks import PermanentCallback
import gobject

"""Hier komt alles in om de applicatie "echt" te laten draaien"""
#@TODO: misschien nog renamen naar app/server?

class Server:
    def __init__(self):
        self.setup_config()
        self.setup_logger()
        self.setup_callbacks()
        self.load_plugins()
        self.setup_player()

        callbacks.RunCallbackChain(Server, 'after_boot', self)

    def setup_config(self):
        self.config = Config()

    def setup_logger(self):
        self.log = Logger(self.config.log)

    def setup_callbacks(self):
        from player import Player
        
        callbacks.RegisterCallback(Player, 'stop',
            PermanentCallback(lambda p: self.log.debug('Stopping.....')))

        callbacks.RegisterCallback(Player, 'play',
            PermanentCallback(lambda p: self.log.debug('Starting playback of %s' % p.current_track)))

        callbacks.RegisterCallback(Player, 'next_track',
            PermanentCallback(lambda p: self.log.debug('Setting next track as current')))
            
        callbacks.RegisterCallback(Player, 'scheduling_new_track',
            PermanentCallback(lambda p: self.log.debug('scheduling new track')))

        callbacks.RegisterCallback(PlayerBackend, 'message',
            lambda m: self.log.debug(m))

        callbacks.RegisterCallback(Server, 'before_loading_plugins',
            PermanentCallback(lambda s: s.log.debug('beginning loading of plugins')))

        callbacks.RegisterCallback(Server, 'after_loading_plugins',
            PermanentCallback(lambda s: s.log.debug('ended loading of plugins')))

    def load_plugins(self):
        callbacks.RunCallbackChain(Server, 'before_loading_plugins', self)

        for plugin in self.config.plugins:
            exec('from plugins import %s' % plugin)

        callbacks.RunCallbackChain(Server, 'after_loading_plugins', self)

    def setup_player(self):
        self.player = Player()

    def run(self):
        gobject.threads_init()
        self.loop = gobject.MainLoop()
        self.log.debug('running....')
        
        try:
            self.loop.run()
        except (KeyboardInterrupt, SystemExit):
            print 'shuttding down...'
            raise
        except Exception:
            self.log.critical(Exception)
        finally:
            self.stop()

    def stop(self):
        self.loop.quit()
        callbacks.RunCallbackChain(Server, 'after_stop', self)

    run_old = run
    def run(self):
        callbacks.RunCallbackChain(Server, 'before_run', self)
        self.run_old()
        callbacks.RunCallbackChain(Server, 'after_run', self)

    setup_player_old = setup_player
    def setup_player(self):
        callbacks.RunAllCallbacks(Server, 'before_setup_player', self)
        self.setup_player_old()
        callbacks.RunAllCallbacks(Server, 'after_setup_player', self)

callbacks.RegisterCallback(Server, 'before_run',
    PermanentCallback(lambda s: s.log.debug('yep, before_run is called')))