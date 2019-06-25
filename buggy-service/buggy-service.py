#!/usr/bin/env python3
from socketserver import TCPServer, BaseRequestHandler
from threading import Thread


class NoDataTcpHandler(BaseRequestHandler):
    def handle(self):
        print("Nothing", flush=True)
        print(self.request.recv(1024).decode("utf-8"), flush=True)


class WeirdAnswerHandler(BaseRequestHandler):
    def handle(self):
        print("Weird", flush=True)
        self.request.sendall("Hello".encode("utf-8"))


class StaticHttpResponse(BaseRequestHandler):
    def handle(self):
        print("Static", flush=True)
        print(self.request.recv(1024).decode("utf-8"))
        self.request.sendall(
            "HTTP/1.1 200 OK\n"
            "Content-Type: text/plain\n"
            "Content-Length: 6\n"
            "\n"
            "Hello\n".encode("utf-8")
        )


# Emulate an HTTP server that closes the connexion instantly
if __name__ == "__main__":
    print("Starting buggy service", flush=True)

    host = "0.0.0.0"
    servers = (
        TCPServer((host, 8000), NoDataTcpHandler),
        TCPServer((host, 8001), WeirdAnswerHandler),
        TCPServer((host, 8002), StaticHttpResponse)
    )

    threads = [Thread(target=server.serve_forever) for server in servers]

    for thread in threads: thread.start()

    print("Everything started.", flush=True)
    for thread in threads: thread.join()
