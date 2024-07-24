import socketserver
from routes import routes
import pymongo
import os


mongo_uri = f"mongodb://{os.environ["MONGO_USERNAME"]}:{os.environ["MONGO_PASSWORD"]}@{os.environ["MONGO_HOST"]}:{os.environ["MONGO_PORT"]}/?authSource=admin"
client = pymongo.MongoClient(mongo_uri)
db = client.chat_app_db
# collection = db.test_collection
# entry = {"x": 10}
# collection.insert_one(entry)
# print(collection.find_one({"x": 10}))

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):

        # construct request and response
        routes(self, db)

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
