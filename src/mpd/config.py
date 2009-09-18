from attr import *
#from configparse import OptionParser
#from configparse import OptionGroup
##http://www.gustaebel.de/lars/configparse/
#from listoption import ListOption
from parser import Parser

class Config(object):
    attr_accessor(opts = [])
    #parser = OptionParser(option_class=ListOption)
    parser = Parser()

    def __init__(self):
        # Read this option from both the command line and the config file (config="true").
        Config.parser.add_option("-p", "--plugins", action="store", type="list",
            #dest="plugins", default=[], help="...", config="true")
            dest="plugins", default=[], help="list of modules living in mpd/plugins/")

        opts, args = Config.parser.parse_args()
        self.opts = opts

    def __getattr__(self, name):
        return getattr(self.opts, name)
