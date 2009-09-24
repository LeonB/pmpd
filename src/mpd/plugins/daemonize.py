#from supay import Daemon
import daemon
import callbacks
from mpd.server import Server

#sys.path

class Daemonize(object):
    def run(self, server):
        import daemon
        daemon.daemonize(True)
        server.log.debug('Daemonized succeeded')

    def stop(self, server):
        daemon.stop()

callbacks.RegisterCallback(Server, 'after_boot', Daemonize().run)