from util.http_utils import split_request, split_header, extract_headers


def buffer(socket):
    buffer_size = 8192

    data = socket.request.recv(buffer_size)

    print(socket.client_address)
    print("--- received data ---")
    print(data)
    print("--- end of data ---\n\n")

    header, body = split_request(data)
    request_line, headers = split_header(header)
    headers = extract_headers(headers)

    if "Content-Length" in headers:
        expected_len = (
            len(header.encode())
            + len("\r\n\r\n".encode())
            + int(headers["Content-Length"])
        )
        remaining_len = expected_len - len(data)

        if remaining_len > 0:

            while len(data) < expected_len:

                new_data = socket.request.recv(buffer_size)
                data += new_data

    return data
