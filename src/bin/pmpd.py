import sys
sys.path.append('.')
sys.path.append('./libs')

import mpd as MPD
MPD.Server().run()