from mpd.player_backend import PlayerBackend
import gst
import gobject
import callbacks

gobject.threads_init()

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
            self.playbin.set_state(gst.STATE_NULL)
            #self.loop.quit()
            print 'stopped gstreamer'
        elif t == gst.MESSAGE_ERROR:
            print message
            print 'error!'
            #self.loop.quit()
        elif t == gst.MESSAGE_STATE_CHANGED:
            #http://pygstdocs.berlios.de/pygst-reference/class-gstmessage.html
            new_state =  message.parse_state_changed()[1]
            callbacks.RunCallbackChain(PlayerBackend, 'message', new_state)
        else:
            ''
            #print message

    def on_about_to_finish(self, playbin):
        if not self.player.stopped():
            self.player.schedule_next_track()

            if (self.player.current_track):
                track = self.player.current_track
                self.playbin.set_property("uri", 'file://' + track.name)
                self.playbin.set_state(gst.STATE_PLAYING)

    def play(self, track):
        if self.playbin.get_state()[1] == gst.STATE_PLAYING:
            self.playbin.set_state(gst.STATE_NULL)

        self.playbin.set_property("uri", 'file://' + track.name)
        self.playbin.set_state(gst.STATE_PLAYING)

#        self.loop = gobject.MainLoop()
#        context = self.loop.get_context()
#        context.iteration(True)
#        self.loop.run()

    def resume(self):
        self.playbin.set_state(gst.STATE_PLAYING)

    def pause(self):
        self.playbin.set_state(gst.STATE_PAUSED)

    def stop(self):
        #self.playbin.set_state(gst.STATE_NULL)
        #self.playbin.send_event(gst.event_new_eos())
        ''