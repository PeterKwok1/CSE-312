import urllib.parse
from util.connection import db
import json
from util.escape_html import escape_html
from bson.objectid import ObjectId
from util.auth import (
    extract_credentials,
    validate_password,
    generate_auth,
    validate_auth,
    delete_auth,
    generate_xsrf,
    validate_xsrf,
)
from util.spotify_utils import get_current_song
import bcrypt
import os
import urllib
import base64
import re
import uuid
import requests
from util.file_extension import get_file_extension

def return_index(request, response):
    # open template
    template = open("./public/template_index.html", "rt")
    template_str = template.read()

    # visit count
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
    template_update = template_str.replace(r"{{visits}}", str(visit_count))

    # auth
    user = validate_auth(request)
    # xsrf
    if user:
        xsrf_token = generate_xsrf(user["username"])
        template_update = template_str.replace(r"{{xsrf_token}}", str(xsrf_token))

    # save template
    index = open("./public/index.html", "wt")
    index.write(template_update)
    template.close()
    index.close()

    index = open("./public/index.html", "rb")
    return response.send(index)


def return_static_file(request, response):

    # validate
    # only allow intended subdirectories by removing /
    # thinking back, I could have added these as separate routes and abstracted the remove "/" logic. multiple public paths is probably fine. in hindsight, i'd have to break up return_static_file() for each. 
    if re.search("^/public/image/", request.path):
        directory = "/public/image/"
        filename = request.path.replace("/public/image/", "").replace("/", "")
    elif re.search("^/public/user_media/", request.path):
        directory = "/public/user_media/"
        filename = request.path.replace("/public/user_media/", "").replace("/", "")
    elif re.search("^/public/", request.path):
        directory = "/public/"
        filename = request.path.replace("/public/", "").replace("/", "")
    request.path = directory + filename

    try:
        file = open(f".{request.path}", "rb")
    except:
        response.set_status(404)
        return response.send("404: Not Found")

    return response.send(file)


def get_all_messages(request, response):

    messages = list(db.message_collection.find())

    # json data types do not include mongo ObjectId's.
    for i in range(len(messages)):
        messages[i]["id"] = str(messages[i]["_id"])
        del messages[i]["_id"]

    # response.set_status(200)
    return response.send(messages)

def post_message(request, response):
    message = json.loads(request.body)

    # auth
    user = validate_auth(request)
    # xsrf
    if user:
        if not validate_xsrf(user["username"], message["xsrf_token"]):
            response.set_status(403)
            return response.send("submission rejected")

    # user, spotify user, guest
    if user:
        username = user["username"] 
        if "access_token" in user: 
            current_song = get_current_song(user["access_token"])
        else:
            current_song = None
    else:
        username = "Guest"
        current_song = None

    # it wasn't required, but a user could also set their username to html to perform an html injection attack since that's displayed to other users as well.
    message_to_save = {
        "username": username,
        "current_song": current_song,
        "message": escape_html(message["message"]),
    }

    # insert_one returns an InsertOneResult object
    message_save_result = db.message_collection.insert_one(message_to_save)

    # find_one returns dict with objectId
    message_saved = db.message_collection.find_one(
        {"_id": ObjectId(message_save_result.inserted_id)}
    )

    # convert objectId to str to match json format 
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

def post_media(request, response):
    # auth
    user = validate_auth(request)

    # user, spotify user, guest
    if user:
        username = user["username"] 
        if "access_token" in user: 
            current_song = get_current_song(user["access_token"])
        else:
            current_song = None
    else:
        username = "Guest"
        current_song = None
        
    # save file
    file_extension = get_file_extension(request.body.parts[0].content)

    filename = str(uuid.uuid4()) + "." + file_extension

    # Images will be saved to container. 
    with open(f"./public/user_media/{filename}", "wb") as user_media:
        user_media.write(request.body.parts[0].content)
    
    if file_extension == "mp4":
        message = f'<video height="240" width="320" controls autoplay muted alt="{username}\'s media"><source src="/public/user_media/{filename}" type="video/mp4"></video>'
    else:
        message = f'<img src="/public/user_media/{filename}" height="240" width="320" alt="{username}\'s media">'

    message_to_save = {
        "username": username,
        "current_song": current_song,
        "message": message
    }

    # save message
    db.message_collection.insert_one(message_to_save)

    response.set_status(302)
    response.set_header({"Location": "/"})
    
    return response.send()

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


def login_spotify(request, response):
    # get access code
    scope = "user-read-currently-playing user-read-email"
    query = urllib.parse.urlencode(
        {
            "response_type": "code",
            "client_id": os.environ["SPOTIFY_ID"],
            "scope": scope,
            "redirect_uri": "http://localhost:8080/spotify",
        }
    )

    response.set_status(302)
    response.set_header({"Location": "https://accounts.spotify.com/authorize?" + query})

    return response.send()


def spotify(request, response):
    # recieve access code
    if "error" in request.query:
        response.set_status(401)
        return response.send("Error login with spotify")
    

    # get access token
    access_request_body = urllib.parse.urlencode(
        {
            "grant_type": "authorization_code",
            "code": request.query["code"],
            "redirect_uri": "http://localhost:8080/spotify",
        }
    )
    access_request_headers = {
        "Authorization": "Basic" + " " + base64.b64encode(f"{os.environ["SPOTIFY_ID"]}:{os.environ["SPOTIFY_SECRET"]}".encode()).decode(),
        "Content-Type": "application/x-www-form-urlencoded",
    }
    access_response = requests.post("https://accounts.spotify.com/api/token", data=access_request_body, headers=access_request_headers)


    if not access_response.status_code == 200:
        return response.send("Login with spotify failed")
    
    access_response_body = access_response.json()
    access_token = access_response_body["access_token"]

    # get user profile
    user_request_headers = {
        "Authorization": "Bearer" + " " + access_token
    }
    user_response = requests.get("https://api.spotify.com/v1/me", headers=user_request_headers)
    user_response_body = user_response.json()
    email = user_response_body["email"]

    # if no account, make one
    user = db.users.find_one({"username": email})
    if not user:
        db.users.insert_one({"username": email, "access_token": access_token})
    else:
        db.users.update_one({"username": email}, {"$set": {"access_token": access_token}})
    
    test = db.users.find_one({"username": email})

    # generate auth
    response = generate_auth(response, email)

    # spotify access tokens expire in 1 hour, so i'd likely have to refresh it using a refresh token if expired during validation. 

    response.set_status(302)
    response.set_header({"Location": "/"})

    return response.send()

    

    
