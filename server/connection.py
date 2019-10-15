import socket
import json


class Connection:

    def __init__(self):
        self.localAddress = ('127.0.0.1', 65432)
        self.bufferSize = 1024
        self.UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDPServerSocket.bind(self.localAddress)

    def send(self, dataObject, address):
        dataObjectJSON = json.dumps(dataObject)
        dataObjectBytes = str.encode(dataObjectJSON)
        self.UDPServerSocket.sendto(dataObjectBytes, address)
    
    def sendAll(self, dataObject, addresses):
        for address in addresses:
            self.send(dataObject, address)

    def receive(self):
        data, address = self.UDPServerSocket.recvfrom(self.bufferSize)
        dataJSON = data.decode('utf-8')
        dataObject = json.loads(dataJSON)

        return (dataObject, address)
