import sys

def class_space(classlevel=3):
    "returns the calling class' name and dictionary"
    frame = sys._getframe(classlevel)
    classname = frame.f_code.co_name
    classdict = frame.f_locals
    return classname, classdict

def attr_accessor(**keywords):
    return _attribute('rw', **keywords)

def attr_reader(**keywords):
    return _attribute('r', **keywords)

def attr_writer(**keywords):
    return _attribute('w', **keywords)

def attr_accessor(permission='rwd', **kwds):
    """returns one property for each (key,default) pair in kwds;
       each property provides the specified level of access(permission):
           'r': readable, 'w':writable, 'd':deletable
    """
    return _attribute(permission, **kwds)

def _attribute(permission = 'rw', **keywords):
    classname, classdict = class_space()

#    def _property(attrname, default):
#        fget, fset, fdel, doc = None, None, None, None
#
#        def fget(self):
#            return 55
#
#        return property(fget, fset, fdel, doc)

    for attrname, default in keywords.items():
        private_attrname = "__%s" % attrname

        if 'r' in permission:
            def fget(self):
                print private_attrname
                value = default
                try: value = getattr(self, private_attrname)
                except AttributeError: setattr(self, private_attrname, default)
                return value
        if 'w' in permission:
            def fset(self, default):
                setattr(self, attrname, default)
        if 'd' in permission:
            def fdel(self):
                try: delattr(self, attrname)
                except AttributeError: pass
                # calling fget can restore this attribute, so remove property
                delattr(self.__class__, propname)
        #classdict[attrname] = lambda self: default
        classdict["get_" + attrname] = fget
        classdict[attrname] = property(classdict["get_" + attrname])
        #classdict['get_tester2'] = lambda self: default
        #classdict['tester2'] = property(classdict['get_tester2'])

class Tester(object):
    attr_reader(tester2 = 11, tester = 1)

#    def tester2(self):
#        return 12

a = Tester()
#print a.tester()
#print a.tester2()
print a.tester2