from util.connection import db
import json
from util.escape_html import escape_html
from bson.objectid import ObjectId
import datetime


def return_index(request, response):
    visit_count = (
        int(request.cookies["visit_count"]) + 1
        if "visit_count" in request.cookies
        else 1
    )

    ## replaced this with Max-Age directive
    # cookie_expiration = datetime.datetime.now(datetime.UTC) + datetime.timedelta(
    #     hours=1
    # )
    # date_format = r"%a, %d %b %Y %X %Z"
    # response.set_cookie(
    #     {
    #         "visit_count": f"{visit_count}; Expires={cookie_expiration.strftime(date_format)}"
    #     }
    # )

    response.set_cookie({"visit_count": f"{visit_count}; Max-Age={3}; HttpOnly"})

    # i may have just been able to encode the text to bytes.
    template = open("./public/template.html", "rt").read()
    template_update = template.replace(r"{{visits}}", str(visit_count))
    file = open("./public/index.html", "wt")
    file.write(template_update)
    file.close()
    file = open("./public/index.html", "rb")

    return response.send(file)


def return_static_file(request, response):
    file = open(f".{request.path}", "rb")

    return response.send(file)


def get_all_messages(request, response):

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
    return response.send(messages)


def post_message(request, response):
    message = json.loads(request.body)

    message_to_save = {
        "username": "Guest",
        "message": escape_html(message["message"]),
    }

    # insert_one returns an InsertOneResult object
    message_save_result = db.message_collection.insert_one(message_to_save)

    # find_one returns dict with objectId
    message_saved = db.message_collection.find_one(
        {"_id": ObjectId(message_save_result.inserted_id)}
    )

    # convert objectId to str to match json format k
    message_saved["_id"] = str(message_saved["_id"])

    response.set_status(201)
    return response.send(message_saved)


def get_message_by_id(request, response):
    if ObjectId.is_valid(request.params["id"]):

        message = db.message_collection.find_one(
            {"_id": ObjectId(request.params["id"])}
        )

        if message:

            message["_id"] = str(message["_id"])

            response.set_status(200)
            return response.send(message)

    response.set_status(404)
    return response.send("Message not found")


def delete_message_by_id(request, response):
    if ObjectId.is_valid(request.params["id"]):

        delete_result = db.message_collection.delete_one(
            {"_id": ObjectId(request.params["id"])}
        )

        if delete_result.deleted_count:
            response.set_status(204)
            return response.send("Delete Successful")

    response.set_status(404)
    return response.send("Delete Unsuccessful")


def update_message_by_id(request, response):
    if ObjectId.is_valid(request.params["id"]):

        update = json.loads(request.body)

        update_result = db.message_collection.update_one(
            {"_id": ObjectId(request.params["id"])}, {"$set": update}
        )

        if update_result.matched_count:
            # update_one does not return the doc or _id
            updated = db.message_collection.find_one(
                {"_id": ObjectId(request.params["id"])}
            )
            updated["_id"] = str(updated["_id"])

            response.set_status(200)
            return response.send(updated)

    response.set_status(404)
    return response.send("Update Unsuccessful")
