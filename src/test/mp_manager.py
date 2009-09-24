## server.py
from multiprocessing.managers import BaseManager

class Target(object):
  _x = 0
  def get_x(self):
    return self._x
  def set_x(self, x):
    self._x = x

class RemoteManager(BaseManager):
  pass

tgt = Target()
RemoteManager.register('get_target', callable=lambda:tgt)
mgr = RemoteManager(address=('', 50000), authkey='secret')
srv = mgr.get_server()
srv.serve_forever()

#---------------------------------------
## client.py
from multiprocessing.managers import BaseManager

class RemoteManager(BaseManager):
  pass

RemoteManager.register('get_target')
mgr = RemoteManager(address=('', 50000), authkey='secret')
mgr.connect()
tgt = mgr.get_target()
print(tgt.get_x())
tgt.set_x(tgt.get_x() + 1)

