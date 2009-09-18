#!/usr/bin/env python

import sys
sys.path.append('.')
sys.path.append('./libs')

import mpd as MPD

#Start the player
player = MPD.Player()
player.playlist.add('./test/samples/gapless/wav/*.wav')
#player.playlist.add('~/Workspaces/rmpd/test/samples/gapless/04. Beethoven.wav')
#player.playlist.add('/usr/lib/openoffice/basis3.0/share/gallery/sounds/train.wav')
player.play()

import time
#while player.playing():
while True:
    #print "playing #{player.current_track.path}"
    time.sleep(10)
    print 'still running'