from multiprocessing import Process
import time

class Tester(object):
    def __init__(self):
        self.i = 1

    def run(self):
        self.i = 1000000
        time.sleep(2)
        print self.i

t = Tester()
print t.i

p = Process(target=t.run)
p.start()

print t.i
print 'process started'
p.join()
print t.i