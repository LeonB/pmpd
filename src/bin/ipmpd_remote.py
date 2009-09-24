import sys
sys.path.append('.')
sys.path.append('./libs')

import IPython.ipapi
import Pyro.core

Pyro.core.initClient(banner=0)
p = Pyro.core.getProxyForURI("PYROLOC://localhost:7766/pmpd")

#add the player methods
current_track = lambda: p.current_track
play = p.play
state = p.state
next = p.next
stop = p.stop
pause = p.pause
playlist = p.playlist
playing = p.playing
paused = p.paused

#Start the shell
IPython.Shell.IPShell(user_ns=locals()).mainloop()