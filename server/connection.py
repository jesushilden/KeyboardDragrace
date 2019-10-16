import socket
import json


class Connection:

    def __init__(self):
        self.localAddress = ('127.0.0.1', 65432)
        self.bufferSize = 1024
        self.UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDPServerSocket.bind(self.localAddress)

    def sendTriple(self, dataObject, address):
        for _ in range(3):
            self.send(dataObject, address)

    def send(self, dataObject, address):
        dataObjectJSON = json.dumps(dataObject)
        dataObjectBytes = str.encode(dataObjectJSON)
        self.UDPServerSocket.sendto(dataObjectBytes, address)

    def sendAllTriple(self, dataObject, addresses):
        for address in addresses:
            self.sendTriple(dataObject, address)

    def sendAll(self, dataObject, addresses):
        for address in addresses:
            self.send(dataObject, address)

    def receive(self):
        data, address = self.UDPServerSocket.recvfrom(self.bufferSize)
        dataJSON = data.decode('utf-8')
        dataObject = json.loads(dataJSON)

        return (dataObject, address)

    def informClose(self, addresses):
        dataObject = {
            'task': 'CLOSE'
        }
        self.sendAllTriple(dataObject, addresses)
    
    def informEnded(self, winner, addresses):
        dataObject = {
            'task': 'ENDED',
            'winner': winner
        }
        self.sendAllTriple(dataObject, addresses)
    
    def informStarting(self, addresses):
        dataObject = {
            'task': 'STARTING'
        }
        self.sendAllTriple(dataObject, addresses)
    
    def informStarted(self, addresses):
        dataObject = {
            'task': 'STARTED'
        }
        self.sendAllTriple(dataObject, addresses)
    
    def sendGameStatus(self, players, addresses):
        dataObject = {
            'task': 'STATUS',
            'players': players
        }
        self.sendAll(dataObject, addresses)

    def ackJoin(self, address):
        dataObject = {
            'task': 'JOIN',
            'playerAddress': str(address)
        }
        self.sendTriple(dataObject, address)
    
    def ackLeave(self, address):
        dataObject = {
            'task': 'LEAVE'
        }
        self.sendTriple(dataObject, address)
