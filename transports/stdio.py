import sys

def argparser(parser):
    parser = parser.add_argument_group(title = 'tcp')
    parser.add_argument('-s', '--server', action='store_true', dest='beserver', help='Act as server')
    parser.add_argument('-p', '--port', action='store', dest='port', help='Local/Remote port', required=True, type=int)
    parser.add_argument('-a', '--address', action='store', dest='host', help='Local/Remote listen', default='')

class main:
    def __init__(self, tun, args):
        self.tun = tun
        self.netin = sys.stdin
        self.netout = sys.stdout

    def loop(self):
        while True:
            rd = select.select([self.tun, self.net],[],[])[0][0]
            if rd == self.tun:
                # from tun
                data = self.tun.read(1500)
                self.netout.write(data)
            else:
                # from sock
                data = self.netin.read(1500)
                self.tun.write(data)
