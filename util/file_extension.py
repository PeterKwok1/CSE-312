file_extension_key = {
    "jpg": {"file_signature": "FFD8FFE0", "start": 0, "end": 4},
    "png": {"file_signature": "89504E470D0A1A0A", "start": 0, "end": 8},
    "gif": {"file_signature": "47494638", "start": 0, "end": 4},
    "mp4": {"file_signature": "66747970", "start": 4, "end": 8},
}


def get_file_extension(file: bytes) -> str:
    for extension, file_signature in file_extension_key.items():
        if file.startswith(
            bytes.fromhex(file_signature["file_signature"]),
            file_signature["start"],
            file_signature["end"],
        ):
            return extension
