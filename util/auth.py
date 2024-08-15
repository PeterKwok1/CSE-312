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


def decode_url_encoded_str(url_encoded_str: str) -> dict:
    # username_reg=%5E%26_&password_reg=
    key_vals = {}
    for pair in url_encoded_str.split("&"):
        pair = pair.split("=")
        key = pair[0]
        value = pair[1]
        key_vals[key] = value
    return key_vals


def extract_credentials(request: object) -> list:
    request.body
