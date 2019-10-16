import msvcrt
import threading
from connection import Connection

server = Connection()
WAITING, PLAYING, STARTING = 'WAITING', 'PLAYING', 'STARTING'
status = WAITING

server.join()
data, address = server.receive()
myAddress = data['playerAddress']

print('CONNECTED TO THE GAME')
print('--------------------------')
print('NUMBERS CAN BE USED TO EXECUTE FOLLOWING COMMANDS')
print('  1: CLOSE SERVER')
print('  2: LEAVE GAME')
print('WAITING FOR GAME TO START...')


def keyListener():
    while True:
        charBytes = msvcrt.getch()
        if charBytes == b'1':
            server.close()
            break
        elif charBytes == b'2':
            server.leave()
            break
        elif status == PLAYING:
            keys = 'abcdefghijklmnopqrstuvwxyz'
            key = charBytes.decode("utf-8")
            if key in keys:
                server.play(key)


keyListenerThread = threading.Thread(target=keyListener)
keyListenerThread.daemon = True
keyListenerThread.start()


def printPlayers(players):
    for address in players:
        track = list('--------------------')
        track[players[address]['position']] = '|'
        print(address + ': ' + ''.join(track))


def handleLeave():
    print('BYE')
    exit()


def handleStatus(data):
    printPlayers(data['players'])
    if status == PLAYING:
        print('NEXT KEY: ' + data['players'][myAddress]['nextKey'])



def handleStarted():
    global status
    if status == STARTING:
        status = PLAYING
        print('THE GAME HAS STARTED')


def handleStarting():
    global status
    if status == WAITING:
        status = STARTING
        print('A NEW GAME WILL START IN 5 SECONDS')


def handleEnded(data):
    global status
    if status == PLAYING:
        if myAddress == data['winner']:
            print('CONGRATULATIONS YOU WON')
        else:
            print('YOU DID NOT WIN THIS TIME')
        status = WAITING


while True:
    data, address = server.receive()
    task = data['task']

    if task == 'LEAVE' or task == 'CLOSE':
        handleLeave()
    elif task == 'STATUS':
        handleStatus(data)
    elif task == 'STARTED':
        handleStarted()
    elif task == 'STARTING':
        handleStarting()
    elif task == 'ENDED':
        handleEnded(data)
