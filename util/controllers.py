from util.connection import db
import json
from util.escape_html import escape_html


def get_all_messages(self, request, response):

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


def post_message(self, request, response):
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
