from util.http_utils import (
    split_request,
    split_header,
    extract_request_line,
    extract_headers,
)
import re
from util.multipart import parse_multipart


class Request:

    def __init__(self, request: bytes):
        # TODO: parse the bytes of the request and populate the following instance variables

        # parse request
        header, body = split_request(request)

        request_line, headers = split_header(header)

        method, path, http_version = extract_request_line(request_line)

        self.method = method
        self.path = path
        self.http_version = http_version

        self.headers = extract_headers(headers)

        self.cookies = {}
        if "Cookie" in self.headers:
            cookies = self.headers["Cookie"].split(";")
            for cookie in cookies:
                cookie = cookie.split("=", 1)
                self.cookies[cookie[0].strip(" ")] = cookie[1]

        if self.headers.keys() >= {"Content-Type", "Content-Length"}:
            content_type = self.headers["Content-Type"]
            content_length = int(self.headers["Content-Length"])

            self.body = body[0:content_length]

            if content_type == "text/plain;charset=UTF-8":
                self.body = body.decode("utf-8")
            elif content_type == "application/x-www-form-urlencoded":
                self.body = body.decode("utf-8")
            elif re.search("multipart/form-data", content_type):
                self.body = parse_multipart(self)

        self.params = {}

        self.query = {}

    def set_param(self, key: str, value: str):
        self.params[key] = value

    def set_query(self, query_string):
        key_vals = query_string.split("&")
        for key_val in key_vals:
            key, val = key_val.split("=")
            self.query[key] = val


def test1():
    request = Request(
        b"GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\n\r\n"
    )
    assert request.method == "GET"
    assert "Host" in request.headers
    assert (
        request.headers["Host"] == "localhost:8080"
    )  # note: The leading space in the header value must be removed
    assert request.body == b""  # There is no body for this request.
    # When parsing POST requests, the body must be in bytes, not str

    # This is the start of a simple way (ie. no external libraries) to test your code.
    # It's recommended that you complete this test and add others, including at least one
    # test using a POST request. Also, ensure that the types of all values are correct


def test2():
    request = Request(
        b"POST / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\nCookie: SID=31d4d96e407aad42; lang=en-US\r\n\r\nHello"
    )
    assert request.method == "POST"
    assert "Host" in request.headers
    assert request.headers["Host"] == "localhost:8080"
    assert request.body == b"Hello"

    assert request.cookies["SID"] == "31d4d96e407aad42"
    assert request.cookies["lang"] == "en-US"


if __name__ == "__main__":
    test1()
    test2()
