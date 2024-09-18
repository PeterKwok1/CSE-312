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
        # I'm essentially defining middleware here. 
        
        # query
        if re.search("\\?", request.path):
            request.path, query = request.path.split("?")
            request.set_query(query)
            
        # compare
        for path in self.routes.keys():

            # detect params
            param_pattern = re.compile(":[^/]+")
            path_pattern = f"^{re.sub(param_pattern, "[^/]+", path)}$"

            if re.search(path_pattern, request.path):

                if request.method in self.routes[path]:

                    # extract params
                    param_keys = [(i, key) for i, key in enumerate(path.split("/")) if re.search(param_pattern, key)]
                    path_values = request.path.split("/")

                    for key in param_keys:
                        request.set_param(key[1].strip(":"), path_values[key[0]])  
                    
                    return self.routes[path][request.method](request, response)

        response.set_status(404)
        return response.send("404: Not Found")
    

