import sys
sys.path.append('.')
sys.path.append('./libs')

import Pyro.core

Pyro.core.initClient(banner=0)

# you have to change the URI below to match your own host/port.
#jokes = Pyro.core.getProxyForURI("PYROLOC://localhost:7766/jokegen")
jokes = Pyro.core.getProxyForURI("PYROLOC://localhost:7766/pmpd")

print jokes.state()