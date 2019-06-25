#!/usr/bin/env python3
import socket
import argparse
import sys

parser = argparse.ArgumentParser(description="Send piped content as UDP packets")
parser.add_argument("host", type=str, help="destination host")
parser.add_argument("port", type=int, help="destination port")
parser.add_argument("--payload-size", type=int, help="Max packet size", nargs="?", default=1024)

args = parser.parse_args()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

data = sys.stdin.buffer.read(args.payload_size)
while data:
    sock.sendto(data, (args.host, args.port))
    data = sys.stdin.buffer.read(args.payload_size)
