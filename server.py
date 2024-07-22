import socketserver
from routes import routes
import pymongo
import os


mongo_uri = f"mongodb://{os.environ["MONGO_USERNAME"]}:{os.environ["MONGO_PASSWORD"]}@{os.environ["MONGO_HOST"]}:{os.environ["MONGO_PORT"]}/?authSource=admin"
client = pymongo.MongoClient(mongo_uri)
db = client.test
db.my_collection.insert_one({"x": 10})
# print(db.my_collection.find_one({"x": 10}))
# mongodb://myDatabaseUser:D1fficultP%40ssw0rd@mongodb0.example.com:27017/?authSource=admin
# `mongodb://${MONGO_USER}:${MONGO_PASSWORD}@${MONGO_IP}:${MONGO_PORT}/?authSource=admin`


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
