from attr import *
import callbacks
from config import Config

class Logger:
    attr_accessor(logger = None)

    Config.parser.add_option("-l", "--log-level", action="store", type="choice",
        choices = ('debug', 'error', 'info', 'warning', 'critical'),
        dest="log[level]", help="debug, error, info, warning or critical",
        config="true", default="error")

    Config.parser.add_option("-f", "--log-file", action="store", type="string",
        dest="log[file]", help="path to a file", default="./mpd.log", config="true")

    def __init__(self, config):
        import logging
        level = getattr(logging, config['level'].upper())

        logging.basicConfig(filename=config['file'], level=level,)
        self.logger = logging.getLogger('Pmpd')

    def __getattr__(self, name):
        return getattr(self.logger, name)