import gst

def on_about_to_finish(playbin):
    play_song(playbin, 'file:///home/leon/Workspaces/pmpd/samples/gapless/wav/17. Beethoven.wav')

def on_message(self, bus, message):
    t = message.type
    if t == gst.MESSAGE_EOS:
        print 'eos...'

def play_song(playbin, song):
    print 'trying to play %s' % song

    if playbin.get_state()[1] == gst.STATE_PLAYING:
        playbin.set_state(gst.STATE_NULL)
        #playbin.send_event(gst.event_new_eos())
        while playbin.get_state()[1] == gst.STATE_PLAYING:
            ''

    playbin.set_property("uri", song)
    playbin.set_state(gst.STATE_PLAYING)

playbin = gst.element_factory_make("playbin2", 'Pmpd')
fakesink = gst.element_factory_make("fakesink", "fakesink")
playbin.set_property("video-sink", fakesink)
bus = playbin.get_bus()
bus.connect("message", on_message)
playbin.connect('about-to-finish', on_about_to_finish)

play_song(playbin, 'file:///home/leon/Workspaces/pmpd/samples/gapless/wav/01. Beethoven.wav')
play_song(playbin, 'file:///home/leon/Workspaces/pmpd/samples/gapless/wav/02. Beethoven.wav')
play_song(playbin, 'file:///home/leon/Workspaces/pmpd/samples/gapless/wav/03. Beethoven.wav')
play_song(playbin, 'file:///home/leon/Workspaces/pmpd/samples/gapless/wav/04. Beethoven.wav')
play_song(playbin, 'file:///home/leon/Workspaces/pmpd/samples/gapless/wav/05. Beethoven.wav')
play_song(playbin, 'file:///home/leon/Workspaces/pmpd/samples/gapless/wav/06. Beethoven.wav')
play_song(playbin, 'file:///home/leon/Workspaces/pmpd/samples/gapless/wav/07. Beethoven.wav')
play_song(playbin, 'file:///home/leon/Workspaces/pmpd/samples/gapless/wav/08. Beethoven.wav')
play_song(playbin, 'file:///home/leon/Workspaces/pmpd/samples/gapless/wav/09. Beethoven.wav')
play_song(playbin, 'file:///home/leon/Workspaces/pmpd/samples/gapless/wav/10. Beethoven.wav')
play_song(playbin, 'file:///home/leon/Workspaces/pmpd/samples/gapless/wav/11. Beethoven.wav')
play_song(playbin, 'file:///home/leon/Workspaces/pmpd/samples/gapless/wav/12. Beethoven.wav')
play_song(playbin, 'file:///home/leon/Workspaces/pmpd/samples/gapless/wav/13. Beethoven.wav')
play_song(playbin, 'file:///home/leon/Workspaces/pmpd/samples/gapless/wav/14. Beethoven.wav')
play_song(playbin, 'file:///home/leon/Workspaces/pmpd/samples/gapless/wav/15. Beethoven.wav')
play_song(playbin, 'file:///home/leon/Workspaces/pmpd/samples/gapless/wav/16. Beethoven.wav')

import time
while True:
    print playbin.get_state()[1]
    time.sleep(2)