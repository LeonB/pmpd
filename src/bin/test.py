#!/usr/bin/env python

import sys
sys.path.append('.')
sys.path.append('./libs')
#from pmpd import Mpd
import pmpd as Pmpd

Pmpd.Boot()
p = Pmpd.Player()
p.playlist.add('./test/samples/gapless/wav/*.wav')
p.play()

while True:
    ''