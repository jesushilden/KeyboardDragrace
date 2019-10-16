import socket
import json


class Connection:

    def __init__(self):
        self.UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serverAddress = ('127.0.0.1', 65432)
        self.bufferSize = 1024

    def sendTriple(self, dataObject):
        for _ in range(3):
            self.send(dataObject)

    def send(self, dataObject):
        dataObjectJSON = json.dumps(dataObject)
        dataObjectBytes = str.encode(dataObjectJSON)
        self.UDPClientSocket.sendto(dataObjectBytes, self.serverAddress)

    def receive(self):
        data, address = self.UDPClientSocket.recvfrom(self.bufferSize)
        dataJSON = data.decode('utf-8')
        dataObject = json.loads(dataJSON)

        return (dataObject, address)

    def close(self):
        dataObject = {
            'task': 'CLOSE'
        }
        self.sendTriple(dataObject)

    def join(self):
        self.UDPClientSocket.settimeout(1)
        dataObject = {
            'task': 'JOIN'
        }
        response = (None, None)
        for _ in range(5):
            try:
                self.sendTriple(dataObject)
                response = self.receive()
                break
            except socket.timeout:
                pass

        self.UDPClientSocket.settimeout(None)
        return response

    def play(self, key):
        dataObject = {
            'task': 'PLAY',
            'key': key
        }
        self.send(dataObject)

    def leave(self):
        dataObject = {
            'task': 'LEAVE'
        }
        self.sendTriple(dataObject)
