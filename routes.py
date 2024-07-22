from util.request import Request
from util.response import Response
import re
import datetime
import json


def routes(self):
    # parse request
    received_data = self.request.recv(2048)
    print(self.client_address)
    print("--- received data ---")
    print(received_data)
    print("--- end of data ---\n\n")
    request = Request(received_data)

    found = None

    # root
    if request.path == "/":
        if request.method == "GET":
            found = True

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

    # public
    if re.search("^/public/.+", request.path):
        if request.method == "GET":
            found = True

            response = Response()

            file = open(f".{request.path}", "rb")

            self.request.sendall(response.send(file))

    if request.path == "/chat-messages":
        if request.method == "GET":
            found = True

            # pymongo
            # get messages

            response = Response()

        elif request.method == "POST":
            found = True

            message_json = request.body.decode("utf-8")
            message_dict = json.loads(message_json)

            message = {"username": "Guest", "message": message_dict["message"]}

            # pymongo
            # save message

            response = Response()

            response.set_status(201)

    # Not Found
    if not found:
        response = Response()

        response.set_status(404)

        self.request.sendall(response.send("404: Not Found"))
