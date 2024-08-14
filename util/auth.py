percent_encoding_key = {
    "%21": "!",
    "%40": "@",
    "%23": "#",
    "%24": "$",
    "%25": "%",
    "%5E": "^",
    "%26": "&",
    "%2C": ",",
    "%2D": "-",
    "%5F": "_",
    "%3D": "=",
}
# username_reg=%5E%26_&password_reg=


def extract_credentials(request: object) -> list:
    url_encoded_str = request.body
