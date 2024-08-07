import socketserver
from routes import routes

from util.router import Router
from util.request import Request

app = Router

app.add_route()


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):

        # parse request
        received_data = self.request.recv(2048)
        print(self.client_address)
        print("--- received data ---")
        print(received_data)
        print("--- end of data ---\n\n")
        request = Request(received_data)

        # route request
        app.route_request(request)
        # construct request and response
        # routes(self)
        # test

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
