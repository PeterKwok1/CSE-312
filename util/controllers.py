from util.connection import db
import json
from util.escape_html import escape_html
from bson.objectid import ObjectId
import datetime
from util.auth import (
    extract_credentials,
    validate_password,
    generate_auth,
    validate_auth,
    delete_auth,
)
import bcrypt


def return_index(request, response):
    visit_count = (
        int(request.cookies["visit_count"]) + 1
        if "visit_count" in request.cookies
        else 1
    )

    ## replaced by Max-Age directive
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

    # there maybe a cleaner way to template
    template = open("./public/template_index.html", "rt").read()
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

    # validate
    user = validate_auth(request)
    username = user["username"] if user else "Guest"

    # it wasn't required, but a user could also set their username to html to perform an html injection attack since that's displayed to other users as well.
    message_to_save = {
        "username": username,
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

    # validate
    # if user is valid and message belongs to them, delete
    user = validate_auth(request)
    if not user:
        response.set_status(403)
        return response.send("Not authorized")

    if not ObjectId.is_valid(request.params["id"]):
        response.set_status(404)
        return response.send("Invalid id")

    message = db.message_collection.find_one({"_id": ObjectId(request.params["id"])})
    if not message:
        response.set_status(404)
        return response.send("Message not found")

    if user["username"] == message["username"]:
        db.message_collection.delete_one({"_id": ObjectId(request.params["id"])})

        return response.send("Delete successful")

    response.set_status(403)
    return response.send("Not allowed")


def update_message_by_id(request, response):
    if ObjectId.is_valid(request.params["id"]):

        update = json.loads(request.body)
        update["message"] = escape_html(update["message"])

        update_result = db.message_collection.update_one(
            {"_id": ObjectId(request.params["id"])},
            {"$set": update},
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


def register(request, response):
    # extract credentials
    credentials = extract_credentials(request)
    username = credentials[0]
    password = credentials[1]

    # validate user
    user = db.users.find_one({"username": username})

    if user:
        response.set_status(401)
        return response.send("Username taken")

    if not validate_password(password):
        response.set_status(401)
        return response.send("Invalid password")

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    db.users.insert_one({"username": username, "password": hashed_password})

    # authorize user
    response = generate_auth(response, username)

    # send response
    response.set_status(302)
    response.set_header({"Location": "/"})

    return response.send()


# jamjong
# jammyJong123@
def login(request, response):
    # extract credentials
    credentials = extract_credentials(request)
    username = credentials[0]
    password = credentials[1]

    # validate user
    user = db.users.find_one({"username": username})

    if not user:
        response.set_status(401)
        return response.send("Username not found")

    if not bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        response.set_status(401)

        return response.send("Invalid password")

    # authorize user
    response = generate_auth(response, username)

    # send response
    response.set_status(302)
    response.set_header({"Location": "/"})

    return response.send()


def logout(request, response):
    # validate
    delete_result = delete_auth(request)

    if delete_result:
        response.set_status(302)
        response.set_header({"Location": "/"})

        return response.send()
    else:
        return response.send("Logout failed")
