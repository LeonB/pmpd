from copy import copy
from optparse import OptionValueError
from configparse import Option

def check_list(option, opt, value):
    try:
        return value.split(',')
    except ValueError:
        raise OptionValueError(
            "option %s: invalid list value: %r" % (opt, value))

class ListOption (Option):
    TYPES = Option.TYPES + ("list",)
    TYPE_CHECKER = copy(Option.TYPE_CHECKER)
    TYPE_CHECKER["list"] = check_list
