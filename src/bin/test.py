#!/usr/bin/env python

import sys
sys.path.append('.')
sys.path.append('./libs')
#from pmpd import Mpd
import pmpd as Pmpd

Pmpd.Boot()
p = Pmpd.Player()
#p.playlist.add('../samples/gapless/wav/*.wav')
p.playlist.add('/home/leon/Workspaces/pmpd/samples/gapless/wav/02. Beethoven.wav')
p.play()

#while not p.state() == 'stopped':
while True:
    print p.current_track
    print p.state()
    import time
    
    time.sleep(3)
#    print 'pausing....'
#    p.pause()
#
#
#    time.sleep(3)
#    print 'resuming...'
#    p.play()

#    time.sleep(10)
#    p.next()
#    p.next()
#    p.next()
