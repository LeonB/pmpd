from configparse import OptionParser
from configparse import OptionGroup
#http://www.gustaebel.de/lars/configparse/
from listoption import ListOption
import re
import optparse

class Parser(OptionParser):
    def __init__(self):
        return OptionParser.__init__(self, option_class=ListOption)

    def add_option(self, *args, **kwargs):           
#        if kwargs['action'] == 'store':
#            kwargs['action'] = 'callback'
#            kwargs['callback'] = Parser.parse_dict

        return OptionParser.add_option(self, *args, **kwargs)

    def parse_args(self):
        opts, args = OptionParser.parse_args(self)
        
        new_opts = {}
        for k, v in opts.__dict__.items():
            match = re.match('(.*)\[(.*)\]', k)

            if match:
                group = match.group(1)
                opt = match.group(2)

                if not new_opts.has_key(group):
                    new_opts[group] = {}

                if not new_opts[group].has_key(opt):
                    new_opts[group][opt] = {}

                new_opts[group][opt] = v
            else:
                new_opts[k] = v

        opts = optparse.Values()
        opts._update_loose(new_opts)

        return opts, args

    @classmethod
    def parse_dict(cls, option, opt_str, value, parser, *args, **kwargs):
        match = re.match('--(.*)-(.*)', opt_str)

        if match:
            group = match.group(1)
            opt = match.group(2)

            try:
                values = getattr(parser.values, group)
            except AttributeError:
                values = {}

            #parser.values.group[groupname] = value
            values[opt] = value
            setattr(parser.values, group, values)