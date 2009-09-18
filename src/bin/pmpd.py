import sys
import time
sys.path.append('.')
sys.path.append('./libs')

import mpd as MPD
MPD.Server().run()