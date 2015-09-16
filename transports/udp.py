import socket
import select
import os

def argparser(parser):
    parser = parser.add_argument_group(title = 'tcp')
    parser.add_argument('-s', '--server', action='store_true', dest='beserver', help='Act as server', default=False)
    parser.add_argument('-p', '--port', action='store', dest='port', help='Local/Remote port', required=True, type=int)
    parser.add_argument('-a', '--address', action='store', dest='host', help='Local/Remote listen', default='')

class main:
    def __init__(self, tun, args):
        self.tun = tun
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        remote = (args.host, args.port)
        if args.beserver:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(remote)
        self.net = self.sock

    def loop(self):
        addr = (self.args.host, self.args.port)
        while True:
            rd = select.select([self.tun, self.net],[],[])[0][0]
            if rd == self.tun:
                # from tun
                data = os.read(self.tun, 1500)
                self.net.sendto(data, addr)
            else:
                # from sock
                data, addr = self.net.recvfrom(1500)
                os.write(self.tun, data)
