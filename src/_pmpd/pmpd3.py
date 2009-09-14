#!/usr/bin/env python

import os
import sys
import thread
import time

import gobject
import pygst
#pygst.require("0.10")
import gst

class CLI_Main:

    def __init__(self):
        self.player = gst.element_factory_make("playbin2", "player")
        fakesink = gst.element_factory_make("fakesink", "fakesink")
        self.player.set_property("video-sink", fakesink)
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)
        self.player.connect('about-to-finish', self.start_song_two)

    def start_song_two(self, *args):
        filepath = "file://" + sys.argv[1:][1]
        print(self.player.get_property('uri'))
        print filepath
        
        if self.player.get_property('uri') != filepath:
            self.player.set_property("uri", filepath)
            self.player.set_state(gst.STATE_PLAYING)
        else:
            print 'hiero'
            self.playmode = False

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            print 'song ended'
            self.player.set_state(gst.STATE_NULL)
        elif t == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            print "Error: %s" % err, debug
            self.playmode = False

    def start(self):
        filepath = sys.argv[1:][0]

        if os.path.isfile(filepath):
            self.playmode = True
            self.player.set_property("uri", "file://" + filepath)
            self.player.set_state(gst.STATE_PLAYING)
            while self.playmode:
                #print self.playmode
                time.sleep(1)

        time.sleep(1)
        loop.quit()

mainclass = CLI_Main()
thread.start_new_thread(mainclass.start, ())
gobject.threads_init()
loop = gobject.MainLoop()
loop.run()
