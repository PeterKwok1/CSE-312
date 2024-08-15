import re

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
    # decode percent encoding
    # ex: username_reg=%5E%26_&password_reg=password
    # re.escape escapes regex meta characters. though it's not needed here, it has been applied to the key and value.
    key_escaped_percent_encoding_key = dict(
        (re.escape(key), val) for key, val in percent_encoding_key.items()
    )
    pattern = re.compile("|".join(key_escaped_percent_encoding_key.keys()))

    def decode(str):
        str = re.sub(
            pattern,
            lambda match: key_escaped_percent_encoding_key[re.escape(match.group(0))],
            str,
        )
        return str

    # dictionary
    key_vals = {}
    for pair in url_encoded_str.split("&"):
        pair = pair.split("=")
        key = decode(pair[0])
        value = decode(pair[1])
        key_vals[key] = value
    return key_vals


def extract_credentials(request: object) -> list:
    url_encoded_params = decode_url_encoded_str(request.body)
    username = (
        url_encoded_params["username_reg"]
        if "username_reg" in url_encoded_params
        else url_encoded_params["username_login"]
    )
    password = (
        url_encoded_params["password_reg"]
        if "password_reg" in url_encoded_params
        else url_encoded_params["password_login"]
    )
    return [username, password]
