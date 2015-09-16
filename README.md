# Python Tunnel
Use the Linux TUN driver with arbitrary tunnel formats.

# Current tunnels

 * tcp
 * tcp_base64
 * tcp_xor
 * udp
 * http

# Adding new tunnels

Create a file in `tranports/`, see `tcp.py` for an example.

Add the file to `transports/__init__.py` to enable some checking and help
display.

## Requirements

```
def argparser(parser) # add custom arguments
class main:
    def __init__(self, tun, args) # setup
    def loop(self) # shovel traffic between tun and your transport
```
