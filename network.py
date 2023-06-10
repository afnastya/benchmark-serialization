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
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        if socket_type == 'multicast':
            reg_addr = self.sockets['regular'].getsockname()[0]
            sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(reg_addr))
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
                            socket.inet_aton(host) + socket.inet_aton(reg_addr))
        self.sockets[socket_type] = sock
        self.sel.register(sock, selectors.EVENT_READ, socket_type)

    def handle_request(self, sock, mask, socket_type, callback):
        message, address = sock.recvfrom(1024)
        log.info(f"{message} from {address}")

        callback(sock, message.decode(), address)

    
    def run(self, callback):
        while True:
            events = self.sel.select()
            for key, mask in events:
                socket_type = key.data
                self.handle_request(key.fileobj, mask, socket_type, callback)
