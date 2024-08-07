import socketserver

from util.router import Router
from util.request import Request
from util.response import Response
from util.controllers import (
    return_index,
    return_static_files,
    get_all_messages,
    post_message,
    get_message_by_id,
    delete_message_by_id,
    update_message_by_id,
)


app = Router()

app.add_route("GET", "^/$", return_index)
app.add_route("GET", "^/public/.+", return_static_files)
app.add_route("GET", "/chat-messages", get_all_messages)
app.add_route("POST", "/chat-messages", post_message)
app.add_route("GET", "^/chat-messages/.+", get_message_by_id)
app.add_route("DELETE", "^/chat-messages/.+", delete_message_by_id)
app.add_route("PUT", "^/chat-messages/.+", update_message_by_id)


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):

        # parse request
        received_data = self.request.recv(2048)
        print(self.client_address)
        print("--- received data ---")
        print(received_data)
        print("--- end of data ---\n\n")
        request = Request(received_data)

        response = Response()

        # route request
        response_bytes = app.route_request(request, response)
        self.request.sendall(response_bytes)

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
