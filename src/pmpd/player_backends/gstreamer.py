import gst
import gobject

class Gstreamer():

    def __init__(self, player):
        self.player = player
        self.setup()

    def setup(self):
        self.playbin = gst.element_factory_make("playbin2", 'Pmpd')
        fakesink = gst.element_factory_make("fakesink", "fakesink")
	self.playbin.set_property("video-sink", fakesink)

        bus = self.playbin.get_bus()
	bus.add_signal_watch()
	bus.connect("message", self.on_message)
        self.playbin.connect('about-to-finish', self.on_about_to_finish)

    def on_message(self, bus, message):
        t = message.type
	if t == gst.MESSAGE_EOS:
            print 'ending....'
            self.playbin.set_state(gst.STATE_NULL)
        elif t == gst.MESSAGE_ERROR:
            print message
            print 'error!'
            #self.loop.quit()
        elif t == gst.MESSAGE_STATE_CHANGED:
            #http://pygstdocs.berlios.de/pygst-reference/class-gstmessage.html
            new_state =  message.parse_state_changed()[1]
        else:
            ''
            #print message

    def on_about_to_finish(self, playbin):
#        try:
#            next_track = self.player.playlist.get()
#        except Exception:
#            return False
#
#        self.playbin.set_property('uri', 'file://' + next_track.name)
#        self.player.current_track = next_track
        self.player.schedule_next_track()

        if (self.player.current_track):
            self.playbin.set_property('uri', 'file://' + self.player.current_track.name)

    def play(self, uri):
        self.__state = 'playing'
        self.playbin.set_property("uri", 'file://' + uri)
        self.playbin.set_state(gst.STATE_PLAYING)

        gobject.threads_init()
        self.loop = gobject.MainLoop()
        context = self.loop.get_context()
        context.iteration(True)
        self.loop.run()

#        loop = gobject.MainLoop()
#        gobject.threads_init()
#        context = loop.get_context()
#        while 1:
#            context.iteration(True)

    def pause(self):
        self.playbin.set_state(gst.STATE_PAUSED)

    def stop(self):
        self.loop.quit()
        self.playbin.send_event(gst.event_new_eos())
