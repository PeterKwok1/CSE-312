class multipart_body:
    def __init__(self, boundary: str, parts: list) -> None:
        self.boundary = boundary
        self.parts = parts


class multipart_part:
    def __init__(self, headers: dict, name: str, content: bytes) -> None:
        # decode strings
        self.headers = headers
        self.name = name
        self.content = content


def parse_multipart(request: object) -> object:
    # extract boundary
    # parse on boundary
    # for each item, parse headers, name, content
    pass
