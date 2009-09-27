class MpdLayerServer:
    def __init__(self, server):
        self.server = server

    def __getattr__(self, attr):
        return getattr(self.server, attr)