#!/usr/bin/env python3
from socketserver import UDPServer, BaseRequestHandler


class UdpLogHandler(BaseRequestHandler):
    def handle(self):
        print(self.request[0].strip().decode("utf-8"), flush=True)


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 8000
    with UDPServer((HOST, PORT), UdpLogHandler) as server:
        print("Ready to receive UDP packets", flush=True)
        server.serve_forever()
