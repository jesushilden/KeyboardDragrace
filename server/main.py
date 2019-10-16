from time import sleep
import threading
from connection import Connection
from game import Game

print('APPLICATION UP AND RUNNING')
print('--------------------------')

connection = Connection()
game = Game()


def handleClose():
    connection.sendAllTriple({'task': 'CLOSE'}, game.lobby)
    print('CLOSING SERVER')
    exit()


def handleJoin(address):
    if address not in game.lobby:
        game.joinLobby(address)
        connection.sendTriple({'task': 'JOIN', 'playerAddress': str(address)}, address)
        print(str(address) + ' JOINED')


def handleLeave(address):
    if address in game.lobby:
        game.leaveLobby(address)
        connection.sendTriple({'task': 'LEAVE'}, address)
        print(str(address) + ' LEFT')


def handlePlay(data, address):
    key = data['key']
    addressString = str(address)
    if game.status == 'PLAYING' and addressString in game.players:
        win = game.play(addressString, key)
        if win:
            print('ENDING GAME')
            connection.sendAllTriple(
                {'task': 'ENDED', 'winner': addressString}, game.lobby)


def startGame():
    game.status = 'STARTING'
    print('STARTING GAME IN 5 SECONDS')
    connection.sendAllTriple({'task': 'STARTING'}, game.lobby)

    def startGameDelay():
        sleep(5)
        if len(game.lobby) >= 2:
            connection.sendAllTriple({'task': 'STARTED'}, game.lobby)
            game.startGame()
            connection.sendAll(
                {'task': 'STATUS', 'players': game.players}, game.lobby)
            print('GAME STARTED')
        else:
            game.status = 'WAITING'
    startGameThread = threading.Thread(target=startGameDelay)
    startGameThread.daemon = True
    startGameThread.start()


def sendGameStatus():
    connection.sendAll({'task': 'STATUS', 'players': game.players}, game.lobby)


while(True):
    data, address = connection.receive()
    task = data['task']

    if task == 'CLOSE':
        handleClose()
    elif task == 'JOIN':
        handleJoin(address)
        if game.status == 'PLAYING':
            continue
    elif task == 'LEAVE':
        handleLeave(address)
        continue
    elif task == 'PLAY':
        handlePlay(data, address)

    if game.status == 'WAITING' and len(game.lobby) >= 2:
        startGame()

    if game.status == 'PLAYING':
        sendGameStatus()
