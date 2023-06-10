import selectors
import socket
import logging as log
import time

log.basicConfig(level=log.INFO)

class UdpNetwork:
    def __init__(self):
        self.sel = selectors.DefaultSelector()
        self.sockets = dict()
    
    def add_socket(self, host, port, socket_type='regular'):
        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        sock.bind((host, port))
        self.sockets[socket_type] = socket
        self.sel.register(sock, selectors.EVENT_READ, socket_type)

    def handle_request(self, sock, mask, socket_type, callback):
        message, address = sock.recvfrom(1024)
        log.info(f"{message} from {address}")

        callback(sock, message.decode(), address)

    
    def sendto(self, message, address):
        if 'regular' not in self.sockets:
            return
        self.sockets['regular'].sendto(message.encode(), address)
    
    def run(self, callback):
        while True:
            events = self.sel.select()
            for key, mask in events:
                socket_type = key.data
                self.handle_request(key.fileobj, mask, socket_type, callback)
