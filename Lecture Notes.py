import socketserver


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        recieved_data = self.request.recv(2048)

        client_id = self.client_address[0] + ":" + str(self.client_address[1])
        print(client_id + " is sending data:")
        print(len(recieved_data))
        print(recieved_data)
        print(recieved_data.decode())

        print("\n\n")

        self.request.sendall(
            "HTTP/1.1 200 OK\r\nContent-Length: 5\r\nContent-Type: text/plain: charset=utf-8\r\n\r\nhello".encode()
        )


if __name__ == "__main__":
    host = "0.0.0.0"  # localhost
    port = 8000

    server = socketserver.ThreadingTCPServer((host, port), MyTCPHandler)
    server.serve_forever()
