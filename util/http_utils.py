def split_request(request: bytes) -> list:
    head, body = request.split("\r\n\r\n".encode("utf-8"), 1)
    head = head.decode()
    return [head, body]


def split_header(header: str) -> list:
    return header.split("\r\n", 1)


def extract_request_line(request_line: str) -> list:
    return request_line.split(" ")


def extract_headers(headers_str) -> dict:
    header_dict = {}
    headers_list = headers_str.split("\r\n")
    for header in headers_list:
        header = header.split(":", 1)
        header_dict[header[0]] = header[1].strip(" ")
    return header_dict
