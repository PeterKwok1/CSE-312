from util.connection import db
import json
from util.escape_html import escape_html
from bson.objectid import ObjectId

# could handle db connection errors


def get_all_messages(self, request, response):

    messages = list(db.message_collection.find())

    # json data types do not include mongo ObjectId's.
    messages = [
        {
            "id": str(message["_id"]),
            "username": message["username"],
            "message": message["message"],
        }
        for message in messages
    ]

    response.set_status(200)
    self.request.sendall(response.send(messages))


def post_message(self, request, response):

    message_json = request.body.decode("utf-8")
    message = json.loads(message_json)

    message_to_save = {
        "username": "Guest",
        "message": escape_html(message["message"]),
    }

    message_save_result = db.message_collection.insert_one(message_to_save)

    # convert saved message to dict with json format and send back
    # insert_one returns an InsertOneResult object
    message_saved = db.message_collection.find_one(
        {"_id": ObjectId(message_save_result.inserted_id)}
    )
    message_saved["_id"] = str(message.get("_id"))

    response.set_status(201)
    self.request.sendall(response.send(message_saved))


def get_message_by_id(self, param_id, request, response):
    if ObjectId.is_valid(param_id):

        message = db.message_collection.find_one({"_id": ObjectId(param_id)})

        if message:

            message["_id"] = str(message["_id"])

            response.set_status(200)
            self.request.sendall(response.send(message))
            return

    response.set_status(404)
    self.request.sendall(response.send("Message not found"))


def delete_message_by_id(self, param_id, request, response):
    if ObjectId.is_valid(param_id):

        delete_result = db.message_collection.delete_one({"_id": ObjectId(param_id)})

        if delete_result.deleted_count:
            response.set_status(204)
            self.request.sendall(response.send("Delete Successful"))
            return

    response.set_status(404)
    self.request.sendall(response.send("Delete Unsuccessful"))


def update_message_by_id(self, param_id, request, response):
    if ObjectId.is_valid(param_id):

        update_json = request.body.decode("utf-8")
        update = json.loads(update_json)

        update_result = db.message_collection.update_one(
            {"_id": ObjectId(param_id)}, update
        )

        if update_result.matched_count:
            print(update_result.raw_result)
            # updated = db.message_collection.find_one(
            #     {"_id": ObjectId(message_save_result.inserted_id)}
            # )
            # updated["_id"] = str(message["_id"])

            response.set_status(200)
            self.request.sendall(response.send({}))
            return

    response.set_status(404)
    self.request.sendall(response.send("Update Unsuccessful"))
