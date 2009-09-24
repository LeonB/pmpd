#!/usr/bin/env python

import sys
sys.path.append('.')
sys.path.append('./libs')
#from pmpd import Mpd
import mpd as MPD
import time

s = MPD.Server()

s.log.debug('starting player')

p = MPD.Player()

s.log.debug('player started')

p.playlist.add('../samples/gapless/ogg/*.ogg')
p.next()
p.next()
p.next()
p.next()
p.next()
p.next()
p.next()
p.next()
p.next()
p.playlist.add('/home/leon/Workspaces/pmpd/samples/gapless/wav/09. Beethoven.wav')
p.play()

import time
while True:
    time.sleep(3)