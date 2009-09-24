import os
import mglob
import Queue

class Playlist(Queue.Queue):
    def add(self, input):
        clss = input.__class__

        #Array
        if clss == list:
          for x in input:
            self.add(x)

        #String
        elif clss == str:
            input = os.path.expanduser(input)

            if os.path.isfile(input):
                input = os.path.abspath(input)
                self.add_file(file(input))
            elif os.path.isdir(input):
                self.add_dir(input)
            else:
                files = mglob.expand(input)
                files.sort()

                for i in files:
                    if not os.path.isfile(i) and not os.path.isdir(i):
                        files.remove(i)
                    else:
                        self.add(i)

        #File
        elif clss == file:
            self.add_file(input)

        #directory
        elif clss == dir:
            self.add_dir(input)

    def add_file(self, file):
        self.put(file)

    def add_dir(self, dir):
        for file in os.listdir(dir):
            path = dir + file
            self.add_file(path)

    def get(self, block = False):
        return Queue.Queue.get(self, block)