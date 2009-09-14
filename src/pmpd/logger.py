from attr import *
import callbacks

class Logger:
    attr_accessor(logger = None)

    def __init__(self):
        import logging
        logging.basicConfig(filename='/tmp/logging_example.out',level=logging.DEBUG,)
        self.logger = logging.getLogger('Pmpd')

    def __getattr__(self, name):
        return getattr(self.logger, name)