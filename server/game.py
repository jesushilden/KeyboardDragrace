import uuid
import random
import copy


class Game:

    keys = 'abcdefghijklmnopqrstuvwxyz'

    def __init__(self):
        self.lobby = []
        self.players = {}
        self.goalPosition = 20
        self.status = 'WAITING'

    def joinLobby(self, address):
        self.lobby.append(address)

    def startGame(self):
        self.status = 'PLAYING'

        for address in self.lobby:
            self.players[str(address)] = {
                'position': 0,
                'nextKey': random.choice(self.keys)
            }

    def play(self, addressString, key):
        player = self.players[addressString]

        if key == player['nextKey']:
            player['position'] += 1
            player['nextKey'] = random.choice(self.keys)

        if player['position'] >= self.goalPosition:
            self.status = 'WAITING'
            self.players = {}
            return True
        else:
            return False

    def leaveLobby(self, address):
        self.lobby.remove(address)
