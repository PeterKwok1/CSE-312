from util.request import Request
from util.response import Response
import re
import datetime
import json
from util.escape_html import escape_html
from bson.objectid import ObjectId


def routes(self, db):
    # parse request
    received_data = self.request.recv(2048)
    print(self.client_address)
    print("--- received data ---")
    print(received_data)
    print("--- end of data ---\n\n")
    request = Request(received_data)

    # root
    if request.path == "/":
        if request.method == "GET":
            response = Response()

            visit_count = (
                int(request.cookies["visit_count"]) + 1
                if "visit_count" in request.cookies
                else 1
            )
            cookie_expiration = datetime.datetime.now(
                datetime.UTC
            ) + datetime.timedelta(hours=1)
            date_format = r"%a, %d %b %Y %X %Z"
            response.set_cookie(
                {
                    "visit_count": f"{visit_count}; Expires={cookie_expiration.strftime(date_format)}"
                }
            )

            template = open("./public/template.html", "rt").read()
            template_update = template.replace(r"{{visits}}", str(visit_count))
            file = open("./public/index.html", "wt")
            file.write(template_update)
            file.close()
            file = open("./public/index.html", "rb")

            self.request.sendall(response.send(file))
            return

    # public
    if re.search("^/public/.+", request.path):
        if request.method == "GET":
            response = Response()

            file = open(f".{request.path}", "rb")

            self.request.sendall(response.send(file))
            return

    if request.path == "/chat-messages":
        if request.method == "GET":
            response = Response()

            # pymongo
            # get messages
            messages = list(db.message_collection.find())

            # json data types do not include mongo ObjectId's.
            messages_to_send = [
                {
                    "id": str(message.get("_id")),
                    "username": message["username"],
                    "message": message["message"],
                }
                for message in messages
            ]

            response.set_status(200)
            self.request.sendall(response.send(messages_to_send))
            return

        elif request.method == "POST":
            response = Response()

            message_json = request.body.decode("utf-8")
            message = json.loads(message_json)

            message_to_save = {
                "username": "Guest",
                "message": escape_html(message["message"]),
            }

            message_save_result = db.message_collection.insert_one(message_to_save)

            # convert saved message to dict with json format (similar to above) and send back result
            # insert_one returns an InsertOneResult object
            message_to_send = {
                "id": str(message_save_result.inserted_id),
                "username": message_to_save["username"],
                "message": message_to_save["message"],
            }

            response.set_status(201)
            self.request.sendall(response.send(message_to_send))
            return

    # params
    if re.search("^/chat-messages/.+", request.path):
        if request.method == "GET":
            response = Response()

            param_id = re.search("(?<=^/chat-messages/).+", request.path).group()

            if ObjectId.is_valid(param_id):
                message = db.message_collection.find_one({"_id": ObjectId(param_id)})
                if message:
                    message_to_send = {
                        "id": str(message.get("_id")),
                        "username": message["username"],
                        "message": message["message"],
                    }

                    response.set_status(200)
                    self.request.sendall(response.send(message_to_send))
                    return

            response.set_status(404)
            self.request.sendall(response.send())
            return

        elif request.method == "DELETE":
            response = Response()

            param_id = re.search("(?<=^/chat-messages/).+", request.path).group()

            if ObjectId.is_valid(param_id):
                delete_result = db.message_collection.delete_one(
                    {"_id": ObjectId(param_id)}
                )
                #
                print(delete_result, delete_result.deleted_count)

            response.set_status(204)
            self.request.sendall(response.send())
            return

    # Not Found
    response = Response()
    response.set_status(404)
    self.request.sendall(response.send("404: Not Found"))
