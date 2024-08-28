import json
import re

status_code_key = {
    200: "OK",
    201: "Created",
    204: "No Content",
    404: "Not Found",
    401: "Unauthorized",
    403: "Forbidden",
}
content_type_key = {
    "str": "text/plain; charset=UTF-8",
    "json": "application/json",
    "html": "text/html; charset=UTF-8",
    "css": "text/css; charset=UTF-8",
    "js": "text/javascript",
    "jpg": "image/jpeg",
    "ico": "image/vnd.microsoft.icon",
}


class Response:
    def __init__(self) -> None:
        self.HTTP_Version = "HTTP/1.1"
        self.status_code = 200
        self.reason_phrase = status_code_key[self.status_code]
        self.headers = {"X-Content-Type-Options": "nosniff"}

    def __str__(self) -> str:
        return f"{self.HTTP_Version} {self.status_code} {self.reason_phrase}\r\n{self.headers.items()}"

    def set_status(self, status_code: int):
        self.status_code = status_code
        self.reason_phrase = status_code_key[self.status_code]

    def set_header(self, header: dict):
        for key, value in header.items():
            self.headers[key] = value

    def set_cookie(self, cookie: dict):
        if "Set-Cookie" not in self.headers:
            self.headers["Set-Cookie"] = {}
        for key, value in cookie.items():
            self.headers["Set-Cookie"][key] = value

    def send(self, body="") -> bytearray:

        # body
        if isinstance(body, str):
            self.set_header({"Content-Type": content_type_key["str"]})
            body = body.encode("utf-8")
        elif isinstance(body, dict) or isinstance(body, list):
            self.set_header({"Content-Type": content_type_key["json"]})
            body = json.dumps(body).encode("utf-8")
        else:
            file_extension = re.search("(?<=\\.)[^\\.]+$", body.name).group()
            self.set_header({"Content-Type": content_type_key[file_extension]})
            body = body.read()
        self.headers["Content-Length"] = len(body)

        # request line
        request_line = f"{self.HTTP_Version} {self.status_code} {self.reason_phrase}"

        # headers
        headers = ""
        for key, value in self.headers.items():
            if key == "Set-Cookie":
                for cookie_key, cookie_value in value.items():
                    headers += f"{key}: {cookie_key}={cookie_value}\r\n"
            else:
                headers += f"{key}: {value}\r\n"

        response = (request_line + "\r\n" + headers + "\r\n").encode("utf-8") + body

        return response
