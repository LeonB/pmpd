import sys
sys.path.append('.')
sys.path.append('./libs')

import mpd as MPD
import IPython.ipapi
#print "launching IPython instance"

#Start the player
s = MPD.Server()
p = MPD.Player()

#add the player methods

#Start the player
p = MPD.Player()
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