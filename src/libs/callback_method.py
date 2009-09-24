import callbacks

def callback_method(what, *args):
    def with_callback_method(self):
        methodname = what.__name__
        callbacks.RunCallbackChain(self.__class__, 'before_' + methodname, self)
        result = what(self)
        callbacks.RunCallbackChain(self.__class__, 'before_' + methodname, self)
        return result
    return with_callback_method