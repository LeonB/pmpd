""" attr.py
Provides functions for creating simple properties.

If, inside a class definition, you write:

    attr_accessor(foo=1, bar=2)
    
simple properties named 'foo' and 'bar' are created for this class.
Also, private instance variables '__foo' and '__bar' will be added 
to instances of this class.

USEAGE:

# assumes attr.py is on path
from attr import *

class MyClass(object):
    attr_reader(foo=1, bar=2) # or, attr_accessor('r', foo=1, bar=2)
    attr_writer(fro=3, boz=4) # or, attr_accessor('w', fro=3, boz=4)
    attr_accessor(baz=5)

This is equivalent to the following:

class MyClass(object):
    def __init__(self): 
        self.__foo = 1
        self.__bar = 2
        self.__fro = 3
        self.__boz = 4
        self.__baz = 5

    def get_foo(self): 
        return self.__foo
    def get_bar(self): 
        return self.__bar
    def set_fro(self, value): 
        self.__fro = value
    def set_boz(self, value): 
        self.__boz = value
    def get_baz(self):
        return self.__baz
    def set_baz(self, value):
        self.__baz = value
    def del_baz(self):
        del self.__baz

    foo = property(fget=get_foo, doc="foo")
    bar = property(fget=get_bar, doc="bar")
    fro = property(fset=set_fro, doc="fro")
    boz = property(fset=set_boz, doc="boz")
    baz = property(fget=get_baz, fset=set_baz, fdel=del_baz, doc="baz")
"""

__all__ = ['attr_accessor', 'attr_reader', 'attr_writer']
__version__ = '3.0'
__author__ = 'Leon Bogaert'
__credits__ = ['Sean Ross', 'Guido van Rossum', 'Garth Kidd']
__created__ = '07-09-2009'

import sys

def mangle(classname, attrname):
    """mangles name according to python name-mangling
       conventions for private variables"""
    #return "_%s__%s" % (classname, attrname)
    return "__%s" % attrname

def class_space(classlevel=3):
    "returns the calling class' name and dictionary"
    frame = sys._getframe(classlevel)
    classname = frame.f_code.co_name
    classdict = frame.f_locals
    return classname, classdict

# convenience function
def attr_reader(**kwds):
    "returns one read-only property for each (key,value) pair in kwds"
    return _attribute(permission='r', **kwds)

# convenience function
def attr_writer(**kwds):
    "returns one write-only property for each (key,value) pair in kwds"
    return _attribute(permission='w', **kwds) 

# needed because of the way class_space is resolved in _attribute
def attr_accessor(permission='rwd', **kwds):
    """returns one property for each (key,value) pair in kwds;
       each property provides the specified level of access(permission):
           'r': readable, 'w':writable, 'd':deletable
    """
    return _attribute(permission, **kwds)

# based on code by Guido van Rossum, comp.lang.python 2001-07-31        
def _attribute(permission='rwd', **kwds):
    """returns one property for each (key,value) pair in kwds;
       each property provides the specified level of access(permission):
           'r': readable, 'w':writable, 'd':deletable
    """

    classname, classdict = class_space()
    def _property(classdict, attrname, default):
        attrname, private_attrname = attrname, mangle(classname, attrname)

        fget, fset, fdel, doc = None, None, None, attrname
        if 'r' in permission:
            def fget(self):
                if not self.__dict__.has_key(private_attrname):
                    setattr(self, private_attrname, default)
                return getattr(self, private_attrname)
            classdict['get_' + attrname] = fget
        if 'w' in permission:
            def fset(self, value):
                setattr(self, private_attrname, value)
            classdict['set_' + attrname] = fset
        if 'd' in permission:
            def fdel(self): 
                try: delattr(self, attrname)
                except AttributeError: pass
                # calling fget can restore this attribute, so remove property 
                delattr(self.__class__, propname)

        return property(fget, fset, fdel, doc)
        
    for attrname, default in kwds.items():
        classdict[attrname] = _property(classdict, attrname, default)

#def tester(a = 2, *args, **kwds):
#    print a
#    print args
#    print kwds
#
#class Player:
#    attr_accessor(baz=5, foo = 3)
#    attr_reader(reader = 7)
#    tester('no_default', foo = 2)
#
#    def set_reader(self, value):
#        self.reader = value
#
#p = Player()
#print p.baz
#print p.get_baz()
#p.set_baz(12)
#print p.baz
#print p.foo
#print p.get_foo()
#
#print p.reader
#p.set_reader(1)
#
##print p.no_default