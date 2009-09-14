"""Test of playbin2.  Provide two soundfiles as arguments on the command
line."""

import sys
import time

import gobject
import gst

class Main:
    def __init__(self):
        self.player = gst.element_factory_make("playbin2", "player")
        self.player.set_property("volume", 0.1)
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)
        self.player.connect('about-to-finish', self.on_about_to_finish)

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
        elif t == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            print "Error: %s" % err, debug

    def on_about_to_finish(self, playbin):
        self.player.set_property("uri", "file://" + sys.argv[2])

    def start(self):
        filename = sys.argv[1]
        self.player.set_property("uri", "file://" + filename)
        self.player.set_state(gst.STATE_PLAYING)

        loop = gobject.MainLoop()
        context = loop.get_context()

        # If the loop sleeps longer than 1 us (e.g., 2 us), GStreamer
        # seg faults. However, such a short sleep results in a CPU load
        # of 100%.  Blocking works, but then it is not possible to monitor
        # other events (not shown, but simulated with the sleep).
        while True:
            while context.pending():
                context.iteration(False)
            # Monitor sockets here.
            time.sleep(0.000001)
        #may_block = True
        #while True:
            #context.iteration(may_block)

player = Main()
player.start() 
