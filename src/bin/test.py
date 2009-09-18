#!/usr/bin/env python

import sys
sys.path.append('.')
sys.path.append('./libs')
#from pmpd import Mpd
import mpd as MPD

p = MPD.Player()
#p.playlist.add('../samples/gapless/wav/*.wav')
p.playlist.add('/home/leon/Workspaces/pmpd/samples/gapless/wav/02. Beethoven.wav')
p.play()

while not p.state() == 'stopped':
#    print p.current_track
#    print p.state()
    import time
    
    time.sleep(1)
