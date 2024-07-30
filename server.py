import socketserver
from routes import routes


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):

        # construct request and response
        routes(self)

        # TODO: Parse the HTTP request and use self.request.sendall(response) to send your response


def main():
    host = "0.0.0.0"
    port = 8080

    socketserver.TCPServer.allow_reuse_address = True

    server = socketserver.TCPServer((host, port), MyTCPHandler)

    print("Listening on port " + str(port))

    server.serve_forever()


if __name__ == "__main__":
    main()
