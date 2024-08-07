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
        self.routes[HTTP_method].path = response_method

    # route request to loaded routes
    def route_request(self, request: object) -> bytearray:
        pass


ex = Router()

ex.add_route("a", "b", "c")

print(ex)

test = {"^$": "hihi"}
print(test)
