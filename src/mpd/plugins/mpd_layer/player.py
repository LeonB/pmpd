class MpdLayerPlayer:
    def __init__(self, player):
        self.player = player

    def state(self):
        state = self.player.state

        if state == 'stopped':
            return 'stop'
        elif state == 'playing':
            return 'player'
        elif state == 'paused':
            return 'pause'

        return 'stop'

    def __getattr__(self, attr):
        return getattr(self.player, attr)