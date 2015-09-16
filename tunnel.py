import transports

METHOD = transports.types["tcp"]

import os
import sys
import struct
import argparse
from fcntl import ioctl

# only show help for a transport if a transport is selected
def check_type(type):
    if not type in transports.types:
        raise argparse.ArgumentTypeError("{} not a valid type. Use --list to list valid types".format(type))
    return type

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-t', '--transport', action='store', dest='transport', help='Transport Type', type=check_type)
args,_ = parser.parse_known_args()

parser = argparse.ArgumentParser(add_help=not bool(args.transport))
parser.add_argument('-t', '--transport', action='store', dest='transport', help='Transport Type', type=check_type)
args,_ = parser.parse_known_args()

if not args.transport:
    print "Currently available transport types:"
    for type in transports.types:
        print '\t',type
    sys.exit()

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--transport', action='store', dest='transport', help='Transport Type', type=check_type)
parser.add_argument('--list', action='store_true', dest='listtypes', help='List Transport Types', default=False)
transports.types[args.transport].argparser(parser)

args = parser.parse_args()

if args.listtypes:
    print "Currently available transport types:"
    for type in transports.types:
        print '\t',type

TUNSETIFF = 0x400454ca
f = os.open("/dev/net/tun", os.O_RDWR)
ifs = ioctl(f, TUNSETIFF, struct.pack("16sH", "pytun%d", 0x1))
ifname = ifs[:16].strip("\x00")

transport = transports.types[args.transport].main

transport(f, args).loop()
