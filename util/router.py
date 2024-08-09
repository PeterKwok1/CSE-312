import re


class Router:

    def __init__(self) -> None:
        self.routes = {}

    def __str__(self) -> str:
        output = ""
        for key, val in vars(self).items():
            output += str(f"{key} {val}")
        return output

    # loads routes
    def add_route(self, HTTP_method: str, path: str, response_method):
        if path not in self.routes:
            self.routes[path] = {}

        if HTTP_method not in self.routes[path]:
            self.routes[path][HTTP_method] = response_method

    # route request to loaded routes
    def route_request(self, request: object, response: object) -> bytearray:
        for path in self.routes.keys():
            if re.search(path, request.path):
                return self.routes[path][request.method](request, response)

        response.set_status(404)
        return response.send("404: Not Found")
