import sys
sys.path.append('.')
sys.path.append('./libs')

import Pyro.core

Pyro.core.initClient(banner=0)
p = Pyro.core.getProxyForURI("PYROLOC://localhost:7766/pmpd")

print p.state()