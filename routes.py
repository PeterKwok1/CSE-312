from util.request import Request
from util.response import Response
import re
import datetime
from util.controllers import (
    get_all_messages,
    post_message,
    get_message_by_id,
    delete_message_by_id,
    update_message_by_id,
)


def routes(self):
    # parse request
    received_data = self.request.recv(2048)
    print(self.client_address)
    print("--- received data ---")
    print(received_data)
    print("--- end of data ---\n\n")
    request = Request(received_data)

    response = Response()

    # root
    if request.path == "/":
        if request.method == "GET":

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
    elif re.search("^/public/.+", request.path):
        if request.method == "GET":

            file = open(f".{request.path}", "rb")

            self.request.sendall(response.send(file))

    elif request.path == "/chat-messages":
        if request.method == "GET":

            get_all_messages(self, request, response)

        elif request.method == "POST":

            post_message(self, request, response)

    # params
    elif re.search("^/chat-messages/.+", request.path):

        # could also probably create a function to extract params like express by parsing by "/" and mapping some syntax to it. ``` if request path matches route... ```
        # and add it to the request object via method
        # but idk if necessary and if it'll make sense with the rest of the project
        param_id = re.search("(?<=^/chat-messages/).+", request.path).group()

        if request.method == "GET":

            get_message_by_id(self, param_id, request, response)

        elif request.method == "DELETE":

            delete_message_by_id(self, param_id, request, response)

        elif request.method == "PUT":

            update_message_by_id(self, param_id, request, response)

    else:
        # Not Found
        response.set_status(404)
        self.request.sendall(response.send("404: Not Found"))
