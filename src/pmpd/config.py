from attr import *
from configparse import OptionParser
#http://www.gustaebel.de/lars/configparse/
from listoption import ListOption

class Config(object):
    attr_accessor(parser = OptionParser(option_class=ListOption), opts = [])

    def __init__(self):
        # Read this option from both the command line and the config file (config="true").
        self.parser.add_option("-p", "--plugins", action="store", type="list",
            dest="plugins", default=[], help="...", config="true")

        opts, args = self.parser.parse_args()
        self.opts = opts

    def __getattr__(self, name):
        return getattr(self.opts, name)