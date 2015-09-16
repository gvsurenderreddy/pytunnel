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
        self.args = args
        self.sock = socket.socket()
        remote = (args.host, args.port)
        self.remote = remote
        if args.beserver:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(remote)
            self.sock.listen(1)
            self.net, _ = self.sock.accept()
        else:
            self.sock.connect(remote)
            self.net = self.sock

    def loop(self):
        skip = False
        request = (
            "POST / HTTP/1.1\r\n"
            "Host: localhost:8080\r\n"
            "Connection: keep-alive\r\n"
            "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n"
            "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36\r\n"
            "Accept-Encoding: gzip, deflate, sdch\r\n"
            "Accept-Language: en-US,en;q=0.8"
            "\r\n\r\n{}\r\n\r\n")

        response = "HTTP 200 OK\r\n\r\n{}\r\n\r\n"
        while True:
            rd = select.select([self.tun, self.net],[],[])[0][0]
            if rd == self.tun:
                # from tun
                data = os.read(self.tun, 1500)
                self.net.send((response if self.args.beserver else request).format(data.encode('base64')))
            else:
                # from sock
                data = self.net.recv(8192)
                while not data.endswith('\r\n\r\n'):
                    data += self.net.recv(8192)
                if not data: continue
                print data
                # client
                data = data.split('\r\n\r\n')[1].decode('base64')
                os.write(self.tun, data)
