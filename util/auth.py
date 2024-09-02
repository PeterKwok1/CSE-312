import re
from util.connection import db
import secrets
import hashlib

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
    # ex: username_reg=user_%5Ename&password_reg=passw%26rd
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


def validate_password(password: str) -> bool:
    valid = True
    # could also return false but that doesn't tell if you if the password fails other checks
    if len(password) <= 8:
        valid = False

    if not re.search("[a-z]", password):
        valid = False
        # print("lowercase", password)
    if not re.search("[A-Z]", password):
        valid = False
        # print("uppercase", password)
    if not re.search("[0-9]", password):
        valid = False
        # print("number", password)

    # we aren't decoding + into space so we aren't stripping space, though we could strip + I guess, so if a password contains a space, it will be considered invalid.
    special_characters = re.compile(
        "|".join([re.escape(val) for val in percent_encoding_key.values()])
    )
    if not re.search(special_characters, password):
        valid = False
        # print("special character", password)

    invalid_characters = (
        "[^a-zA-Z0-9" + re.escape("".join(percent_encoding_key.values())) + "]"
    )
    if re.search(invalid_characters, password):
        valid = False
        print("invalid character", password)

    return valid


def hash(bytes_to_hash: bytes) -> bytes:
    hash_obj = hashlib.sha256()
    hash_obj.update(bytes_to_hash)
    hash_hex = hash_obj.hexdigest()
    return hash_hex


# fix: am currently sending hash, not token. send token, store hash, check token hash against stored hash
def generate_auth(response: object, username) -> object:
    token = secrets.token_bytes(32)

    hash_hex = hash(token)

    response.set_cookie({"chat_auth": f"{hash_hex}; HttpOnly"})

    db.users.update_one({"username": username}, {"$set": {"auth_token": hash_hex}})

    return response


def validate_auth(request: object) -> bool:
    if "auth_token" in request.cookies:
        user = db.users.find_one({"auth_token": request.cookies["auth_token"]})
        if user:
            return user
    return False


def delete_auth():
    pass
