from util.http_utils import split_request, extract_headers
import re


class multipart_body:
    def __init__(self, boundary: str, parts: list) -> None:
        self.boundary = boundary
        self.parts = parts

    def __str__(self) -> str:
        return {"boundary": self.boundary, "parts": self.parts}


class multipart_part:
    def __init__(self, headers: dict, name: str, content: bytes) -> None:
        # decode strings
        self.headers = headers
        self.name = name
        self.content = content

    def __str__(self) -> str:
        return {"headers": self.headers, "name": self.name, "content": self.content}


def parse_multipart(request: object) -> object:
    # extract boundary from content-type header
    boundary = (
        "--"
        + re.search("boundary=.+", request.headers["Content-Type"])
        .group()
        .split("=")[1]
    ).encode()

    # parse body on boundary
    # because the first and last boundaries are different from the middle boundaries, i'm trimming them first. i cannot trim boundaries before their differences because their differences are not unique to the body.
    # trim first boundary
    request.body = request.body.removeprefix(boundary + "\r\n".encode())
    # trim second boundary
    request.body = request.body.removesuffix(
        "\r\n".encode() + boundary + "--".encode() + "\r\n".encode()
    )
    # split body on middle boundaries
    request.body = request.body.split("\r\n".encode() + boundary + "\r\n".encode())

    # for each part:
    for i, part in enumerate(request.body):
        # split header body
        header, content = split_request(part)
        # extract headers
        headers = extract_headers(header)
        # extract name
        # I don't see a reason to abstract this logic. I only need the name so far and it is slightly different than cookie parsing.
        # Content-Disposition: form-data; name="field_one"
        name = (
            re.search("name=[^ ]+", headers["Content-Disposition"])
            .group()
            .split("=")[1]
        )
        # decode string bodies, else bytes
        if not "Content-Type" in headers:
            content = content.decode()
        # add headers, name, content to object
        request.body[i] = multipart_part(headers, name, content)

    # add boundary, parts to object
    request.body = multipart_body(boundary, request.body)
    # return object
    return request.body


# POST /profile-pic HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\nContent-Length: 246\r\nCache-Control: max-age=0\r\nsec-ch-ua: "Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"\r\nsec-ch-ua-mobile: ?0\r\nsec-ch-ua-platform: "Windows"\r\nUpgrade-Insecure-Requests: 1\r\nOrigin: http://localhost:8080\r\nContent-Type: multipart/form-data; boundary=----WebKitFormBoundaryoTlVpYBiYGonzLkT\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\r\nSec-Fetch-Site: same-origin\r\nSec-Fetch-Mode: navigate\r\nSec-Fetch-User: ?1\r\nSec-Fetch-Dest: document\r\nReferer: http://localhost:8080/\r\nAccept-Encoding: gzip, deflate, br, zstd\r\nAccept-Language: en-US,en;q=0.9\r\n\r\n------WebKitFormBoundaryoTlVpYBiYGonzLkT\r\nContent-Disposition: form-data; name="field_one"\r\n\r\nwater\r\n------WebKitFormBoundaryoTlVpYBiYGonzLkT\r\nContent-Disposition: form-data; name="field_two"\r\n\r\nmelon\r\n------WebKitFormBoundaryoTlVpYBiYGonzLkT--\r\n

# header: Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryoTlVpYBiYGonzLkT
# body: ------WebKitFormBoundaryoTlVpYBiYGonzLkT\r\nContent-Disposition: form-data; name="field_one"\r\n\r\nwater\r\n------WebKitFormBoundaryoTlVpYBiYGonzLkT\r\nContent-Disposition: form-data; name="field_two"\r\n\r\nmelon\r\n------WebKitFormBoundaryoTlVpYBiYGonzLkT--\r\n

# ------WebKitFormBoundaryoTlVpYBiYGonzLkT
# Content-Disposition: form-data; name="field_one"

# water
# ------WebKitFormBoundaryoTlVpYBiYGonzLkT
# Content-Disposition: form-data; name="field_two"

# melon
# ------WebKitFormBoundaryoTlVpYBiYGonzLkT--\r\n
